#!/usr/bin/env python3
"""
🔄 RGIS DATA SYNC
Sync mining survey data from RGIS.com to your master coordinator

This allows:
- Pull MAG survey data from RGIS storage
- Process surveys on YOUR domain
- Sync results back to RGIS
- Distributed data access
"""

import asyncio
import aiohttp
import argparse
import os
import json
from pathlib import Path
from typing import List, Dict, Any
import hashlib
from datetime import datetime


class RGISDataSync:
    """Sync mining data between RGIS.com and your master"""
    
    def __init__(self, rgis_url: str, master_url: str, data_dir: str = "/opt/quetzalcore/data"):
        self.rgis_url = rgis_url.rstrip('/')
        self.master_url = master_url.rstrip('/')
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    async def list_rgis_surveys(self) -> List[Dict[str, Any]]:
        """List all MAG surveys available on RGIS"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.rgis_url}/api/surveys/list",
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        print(f"❌ Could not list RGIS surveys: {response.status}")
                        return []
        except Exception as e:
            print(f"❌ Error connecting to RGIS: {e}")
            return []
    
    async def download_survey(self, survey_id: str, survey_name: str) -> str:
        """Download MAG survey from RGIS"""
        print(f"📥 Downloading {survey_name} from RGIS...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{self.rgis_url}/api/surveys/download/{survey_id}",
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        # Save to local data directory
                        local_path = self.data_dir / survey_name
                        content = await response.read()
                        
                        with open(local_path, 'wb') as f:
                            f.write(content)
                        
                        print(f"✅ Downloaded to {local_path}")
                        return str(local_path)
                    else:
                        print(f"❌ Download failed: {response.status}")
                        return None
        except Exception as e:
            print(f"❌ Download error: {e}")
            return None
    
    async def process_survey_on_master(self, survey_path: str, file_format: str = "csv") -> Dict[str, Any]:
        """Process survey using YOUR master's mining API"""
        print(f"⚙️  Processing survey on master...")
        
        try:
            async with aiohttp.ClientSession() as session:
                with open(survey_path, 'rb') as f:
                    data = aiohttp.FormData()
                    data.add_field('file', f, filename=os.path.basename(survey_path))
                    data.add_field('file_format', file_format)
                    
                    async with session.post(
                        f"{self.master_url}/api/mining/mag-survey",
                        data=data,
                        timeout=aiohttp.ClientTimeout(total=300)
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            print(f"✅ Processing complete!")
                            print(f"   Anomalies found: {result.get('num_drill_targets', 0)}")
                            return result
                        else:
                            error = await response.text()
                            print(f"❌ Processing failed: {error}")
                            return None
        except Exception as e:
            print(f"❌ Processing error: {e}")
            return None
    
    async def upload_results_to_rgis(self, survey_id: str, results: Dict[str, Any]) -> bool:
        """Upload processing results back to RGIS"""
        print(f"📤 Uploading results to RGIS...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.rgis_url}/api/surveys/{survey_id}/results",
                    json=results,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    if response.status == 200:
                        print(f"✅ Results uploaded to RGIS")
                        return True
                    else:
                        print(f"⚠️  Could not upload results: {response.status}")
                        return False
        except Exception as e:
            print(f"⚠️  Upload error: {e}")
            return False
    
    async def sync_survey(self, survey_id: str, survey_name: str, file_format: str = "csv") -> Dict[str, Any]:
        """Complete sync workflow: download → process → upload results"""
        print(f"\n{'='*60}")
        print(f"🔄 SYNCING SURVEY: {survey_name}")
        print(f"{'='*60}\n")
        
        # 1. Download from RGIS
        local_path = await self.download_survey(survey_id, survey_name)
        if not local_path:
            return {"status": "failed", "error": "download failed"}
        
        # 2. Process on YOUR master
        results = await self.process_survey_on_master(local_path, file_format)
        if not results:
            return {"status": "failed", "error": "processing failed"}
        
        # 3. Upload results back to RGIS
        await self.upload_results_to_rgis(survey_id, results)
        
        # 4. Generate summary
        summary = {
            "status": "success",
            "survey_id": survey_id,
            "survey_name": survey_name,
            "processed_at": datetime.now().isoformat(),
            "num_drill_targets": len(results.get('drill_targets', [])),
            "mineral_types": [
                t['mineral_type'] 
                for t in results.get('mineral_discrimination', {}).get('all_targets', [])
            ],
            "local_path": local_path,
            "results": results
        }
        
        # Save summary
        summary_path = self.data_dir / f"{survey_id}_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\n✅ SYNC COMPLETE!")
        print(f"   Summary saved to: {summary_path}")
        
        return summary
    
    async def sync_all_surveys(self):
        """Sync all available surveys from RGIS"""
        print("\n🔄 SYNCING ALL SURVEYS FROM RGIS\n")
        
        # List surveys
        surveys = await self.list_rgis_surveys()
        if not surveys:
            print("❌ No surveys found on RGIS")
            return
        
        print(f"📊 Found {len(surveys)} surveys on RGIS:\n")
        for i, survey in enumerate(surveys, 1):
            print(f"   {i}. {survey.get('name', 'unknown')} ({survey.get('id', 'no-id')})")
        print()
        
        # Sync each survey
        results = []
        for survey in surveys:
            summary = await self.sync_survey(
                survey['id'],
                survey['name'],
                survey.get('format', 'csv')
            )
            results.append(summary)
            await asyncio.sleep(1)  # Rate limit
        
        # Final summary
        print(f"\n{'='*60}")
        print(f"📊 SYNC SUMMARY")
        print(f"{'='*60}\n")
        
        successful = sum(1 for r in results if r['status'] == 'success')
        failed = len(results) - successful
        
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"📁 Data directory: {self.data_dir}")
        print()


async def main():
    parser = argparse.ArgumentParser(
        description="Sync mining survey data from RGIS.com"
    )
    parser.add_argument(
        "--rgis-url",
        default="http://rgis.com:8000",
        help="RGIS.com API URL"
    )
    parser.add_argument(
        "--master-url",
        required=True,
        help="YOUR master coordinator URL (e.g., http://api.yourdomain.com:8000)"
    )
    parser.add_argument(
        "--data-dir",
        default="/opt/quetzalcore/data",
        help="Local data directory"
    )
    parser.add_argument(
        "--survey-id",
        help="Specific survey ID to sync (optional, syncs all if not provided)"
    )
    parser.add_argument(
        "--survey-name",
        help="Survey filename (required if --survey-id provided)"
    )
    
    args = parser.parse_args()
    
    # Create syncer
    syncer = RGISDataSync(
        rgis_url=args.rgis_url,
        master_url=args.master_url,
        data_dir=args.data_dir
    )
    
    # Sync specific survey or all
    if args.survey_id and args.survey_name:
        await syncer.sync_survey(args.survey_id, args.survey_name)
    else:
        await syncer.sync_all_surveys()


if __name__ == "__main__":
    print("=" * 60)
    print("🔄 RGIS DATA SYNC")
    print("   Download → Process → Upload Results")
    print("=" * 60)
    print()
    
    asyncio.run(main())
