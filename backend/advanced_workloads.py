









# class GPU3DWorkload:
        # """

        
        # Calculate GFLOPS (billions of floating point operations per second)
#         gflops = (metrics["total_flops"] / duration) / 1e9
#         metrics["gflops"] = round(gflops, 2)
        
        # Grade based on performance
#         if gflops > 100:
#             grade = "S"
#         elif gflops > 50:
#             grade = "A"
#         elif gflops > 25:
#             grade = "B"
#         elif gflops > 10:
#             grade = "C"
#         else:
#             grade = "D"
        
#         return {
                        # "duration": float(duration),
                        # "metrics": {k: int(v) if k != "peak_memory_mb" and k != "gflops" else float(v) for k, v in metrics.items()},
                        # "grade": grade,
                        # "gflops": float(gflops)
                # }



#         while nonce < max_nonce:
#             hash_input = f"{block_data}{nonce}".encode()
#             hash_output = hashlib.sha256(hash_input).hexdigest()
#             hashes_computed += 1
            
#             if hash_output.startswith(target):
#                 duration = time.time() - start_time
#                 return {
                    # "found": True,
                    # "nonce": nonce,
                    # )),
                # ]
                # 
                # Wait for both to complete (with timeout)
                # #         try:
                # #             results = await asyncio.wait_for(
                # #                 asyncio.gather(*tasks),
                # #                 timeout=duration_seconds
                # #         except asyncio.TimeoutError:
                # #             results = [{"error": "timeout"}, {"error": "timeout"}]
                #         
                # #         duration = time.time() - start_time
                #         
                # # Final resource measurement
                # #         final_cpu = psutil.cpu_percent(interval=0.1)
                # #         final_memory = process.memory_info().rss / 1024 / 1024
                #         
                # #         gpu_result = results[0] if len(results) > 0 else {}
                # #         mining_result = results[1] if len(results) > 1 else {}
                #         
                # # Combined score
                # #         gpu_gflops = gpu_result.get("gflops", 0)
                # #         mining_hash_rate = mining_result.get("hash_rate", 0)
                #         
                # # Normalize scores (GFLOPS and Hash rate on different scales)
                # #         gpu_score = min(gpu_gflops / 100 * 50, 50)  # Max 50 points
                # #         mining_score = min(mining_hash_rate / 1000000 * 50, 50)  # Max 50 points
                #         
                # #         total_score = gpu_score + mining_score
                #         
                # # Grade
                # #         if total_score >= 90:
                # #             grade = "S"
                # #         elif total_score >= 80:
                # #             grade = "A"
                # #         elif total_score >= 70:
                # #             grade = "B"
                # #         elif total_score >= 60:
                # #             grade = "C"
                # #         else:
                # #             grade = "D"
                #         
                # #         return {
                #     "duration": duration,
                #     "gpu_workload": gpu_result,
                #     "mining_workload": mining_result,
                #     "system_metrics": {
                #         "avg_cpu_percent": (initial_cpu + final_cpu) / 2,
                #         "peak_cpu_percent": max(initial_cpu, final_cpu),
                #         "memory_used_mb": final_memory - initial_memory,
                #         "cpu_cores": psutil.cpu_count()
                #     },
                #     "combined_score": total_score,
                #     "grade": grade,
                #     "description": self._grade_description(grade)
                # }
        # Find if any worker found a valid block
#         found_result = next((r for r in results if r.get("found")), None)
        
#         return {
                        # "found": found_result is not None,
                        # "result": found_result,
                        # "total_hashes": total_hashes,
                        # "duration": duration,
                        # "hash_rate": total_hashes / duration if duration > 0 else 0,
                        # "workers": num_workers,
                        # "hashes_per_worker": [r["hashes"] for r in results]
                # }
    
#     async def run_mining_workload(self, 
#                                   difficulty: int = 4,
#                                   num_blocks: int = 5,
#                                   parallel: bool = True,
#                                   num_workers: int = 4) -> Dict:
        # """
#         Run comprehensive mining workload
        
#         Args:
#             difficulty: Number of leading zeros (higher = harder)
#             num_blocks: Number of blocks to mine
#             parallel: Use parallel mining
#             num_workers: Number of parallel workers
        # """
#         start_time = time.time()
#         blocks_mined = []
#         total_hashes = 0
        
#         for block_num in range(num_blocks):
#             block_data = f"Block{block_num}_Timestamp{int(time.time())}_"
            
#             if parallel:
#                 result = await asyncio.get_event_loop().run_in_executor(
#                     None,
#                     lambda: self.parallel_mine(block_data, difficulty, num_workers)
#             else:
#                 result = await asyncio.get_event_loop().run_in_executor(
#                     None,
#                     lambda: self.mine_block(block_data, difficulty)
            
#             blocks_mined.append(result)
#             total_hashes += result.get("total_hashes", result.get("hashes_computed", 0))
        
#         duration = time.time() - start_time
#         hash_rate = total_hashes / duration if duration > 0 else 0
        
        # Grade based on hash rate (hashes per second)
#         if hash_rate > 1000000:  # 1M H/s
#             grade = "S"
#         elif hash_rate > 500000:  # 500K H/s
#             grade = "A"
#         elif hash_rate > 100000:  # 100K H/s
#             grade = "B"
#         elif hash_rate > 50000:   # 50K H/s
#             grade = "C"
#         else:
#             grade = "D"
        
#         return {
                        # "duration": duration,
                        # "blocks_mined": len(blocks_mined),
                        # "total_hashes": total_hashes,
                        # "hash_rate": hash_rate,
                        # "hash_rate_display": self._format_hash_rate(hash_rate),
                        # "grade": grade,
                        # "difficulty": difficulty,
                        # "parallel": parallel,
                        # "workers": num_workers if parallel else 1
                # }
    
        # @staticmethod
#     def _format_hash_rate(hash_rate: float) -> str:
        # """Format hash rate in human-readable form"""
#         if hash_rate > 1e12:
#             return f"{hash_rate/1e12:.2f} TH/s"
#         elif hash_rate > 1e9:
#             return f"{hash_rate/1e9:.2f} GH/s"
#         elif hash_rate > 1e6:
#             return f"{hash_rate/1e6:.2f} MH/s"
#         elif hash_rate > 1e3:
#             return f"{hash_rate/1e3:.2f} KH/s"
#         else:
#             return f"{hash_rate:.2f} H/s"


# class ExtremeCombinedWorkload:
        # """
#     Combines GPU 3D workloads + Crypto mining for ultimate stress test
        # """
    
#     def __init__(self):
#         self.gpu_workload = GPU3DWorkload()
#         self.mining_workload = CryptoMiningWorkload()
    
#     async def run_combined_extreme(self, duration_seconds: int = 30) -> Dict:
        # """
#         Run both 3D and mining workloads simultaneously
#         Push the system to absolute limits
        # """
#         start_time = time.time()
        
        # Monitor system resources
#         process = psutil.Process()
#         initial_cpu = psutil.cpu_percent(interval=0.1)
#         initial_memory = process.memory_info().rss / 1024 / 1024
        
        # Run both workloads in parallel
#         tasks = [
#             asyncio.create_task(self.gpu_workload.run_3d_workload(
#                 matrix_size=256,
#                 num_iterations=50,
#                 ray_count=50000
            # )),
#             asyncio.create_task(self.mining_workload.run_mining_workload(
#                 difficulty=5,
#                 num_blocks=3,
#                 parallel=True,
#                 num_workers=4
            # ))
        # ]
        
        # Wait for both to complete (with timeout)
#         try:
#             results = await asyncio.wait_for(
#                 asyncio.gather(*tasks),
#                 timeout=duration_seconds
#         except asyncio.TimeoutError:
#             results = [{"error": "timeout"}, {"error": "timeout"}]
        
#         duration = time.time() - start_time
        
        # Final resource measurement
#         final_cpu = psutil.cpu_percent(interval=0.1)
#         final_memory = process.memory_info().rss / 1024 / 1024
        
#         gpu_result = results[0] if len(results) > 0 else {}
#         mining_result = results[1] if len(results) > 1 else {}
        
        # Combined score
#         gpu_gflops = gpu_result.get("gflops", 0)
#         mining_hash_rate = mining_result.get("hash_rate", 0)
        
        # Normalize scores (GFLOPS and Hash rate on different scales)
#         gpu_score = min(gpu_gflops / 100 * 50, 50)  # Max 50 points
#         mining_score = min(mining_hash_rate / 1000000 * 50, 50)  # Max 50 points
        
#         total_score = gpu_score + mining_score
        
        # Grade
#         if total_score >= 90:
#             grade = "S"
#         elif total_score >= 80:
#             grade = "A"
#         elif total_score >= 70:
#             grade = "B"
#         elif total_score >= 60:
#             grade = "C"
#         else:
#             grade = "D"
        
#         return {
                        # "duration": duration,
                        # "gpu_workload": gpu_result,
                        # "mining_workload": mining_result,
                        # "system_metrics": {
                        #     "avg_cpu_percent": (initial_cpu + final_cpu) / 2,
                        #     "peak_cpu_percent": max(initial_cpu, final_cpu),
                        #     "memory_used_mb": final_memory - initial_memory,
                        #     "cpu_cores": psutil.cpu_count()
                        # },
                        # "combined_score": total_score,
                        # "grade": grade,
                        # "description": self._grade_description(grade)
                # }
    
        # @staticmethod
#     def _grade_description(grade: str) -> str:
#         descriptions = {
                        # "S": " BEAST MODE - Crushing both GPU and CPU workloads!",
                        # "A": " EXCELLENT - High performance across all workload types",
                        # "B": " VERY GOOD - Solid performance under extreme load",
                        # "C": " GOOD - Handling advanced workloads adequately",
                        # "D": " FAIR - Room for optimization"
                # }
#         return descriptions.get(grade, "Performance measured")
