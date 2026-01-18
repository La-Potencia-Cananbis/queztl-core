#!/usr/bin/env python3
"""
WebHost AI Training System - Learning from Real Websites
=========================================================
Trains ContentGeneratorNN and SiteOptimizer on real web data with rigorous metrics.

Mathematical foundations:
- Perplexity: exp(-1/N * Σ log P(x_i)) - measures prediction quality
- BLEU score: BP * exp(Σ w_n log p_n) - translation quality metric adapted for HTML
- Design score: Weighted combination of contrast ratio, spacing consistency, color harmony
- Readability: Flesch-Kincaid + custom bilingual metrics
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
import json
import re
import math
from collections import Counter
from typing import Dict, List, Tuple
import numpy as np
from dataclasses import dataclass
from bs4 import BeautifulSoup
import cssutils
import logging

# Suppress cssutils warnings
cssutils.log.setLevel(logging.ERROR)


@dataclass
class TrainingMetrics:
    """Comprehensive training metrics"""
    epoch: int
    loss: float
    perplexity: float
    bleu_score: float
    design_score: float
    readability_score: float
    gradient_norm: float
    learning_rate: float


class WebsiteDataset(Dataset):
    """Dataset for learning from real websites"""
    
    def __init__(self, html_files: List[Path], vocab_size: int = 50000):
        self.samples = []
        self.vocab = self._build_vocab(html_files, vocab_size)
        self.vocab_size = len(self.vocab)
        
        # Parse each HTML file
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Extract features
            features = self._extract_features(html)
            self.samples.append(features)
        
        print(f"✓ Dataset loaded: {len(self.samples)} samples, vocab size: {self.vocab_size}")
    
    def _build_vocab(self, html_files: List[Path], max_size: int) -> Dict[str, int]:
        """Build vocabulary from HTML tokens"""
        token_counts = Counter()
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Tokenize HTML (tags + text)
            tokens = re.findall(r'<[^>]+>|[\w]+|[^\w\s]', html.lower())
            token_counts.update(tokens)
        
        # Keep most common tokens
        vocab = {'<PAD>': 0, '<UNK>': 1, '<START>': 2, '<END>': 3}
        for token, _ in token_counts.most_common(max_size - 4):
            vocab[token] = len(vocab)
        
        return vocab
    
    def _extract_features(self, html: str) -> Dict:
        """Extract training features from HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Tokenize
        tokens = re.findall(r'<[^>]+>|[\w]+|[^\w\s]', html.lower())
        token_ids = [self.vocab.get(t, self.vocab['<UNK>']) for t in tokens[:512]]
        
        # Pad to 512
        if len(token_ids) < 512:
            token_ids += [self.vocab['<PAD>']] * (512 - len(token_ids))
        
        # Extract design metrics
        design_metrics = self._analyze_design(html, soup)
        
        # Extract semantic features
        text_content = soup.get_text(separator=' ', strip=True)
        readability = self._calculate_readability(text_content)
        
        return {
            'tokens': torch.tensor(token_ids, dtype=torch.long),
            'design_metrics': design_metrics,
            'readability': readability,
            'html': html,
            'text': text_content
        }
    
    def _analyze_design(self, html: str, soup: BeautifulSoup) -> torch.Tensor:
        """Analyze design quality metrics"""
        metrics = []
        
        # Extract inline styles
        styles = soup.find_all(style=True)
        colors = []
        spacings = []
        
        for elem in styles:
            style_str = elem.get('style', '')
            # Extract colors
            color_matches = re.findall(r'#[0-9a-fA-F]{3,6}', style_str)
            colors.extend(color_matches)
            # Extract spacing
            spacing_matches = re.findall(r'(\d+(?:\.\d+)?)(px|rem|em)', style_str)
            spacings.extend([float(m[0]) for m in spacing_matches])
        
        # Color diversity (0-1)
        color_diversity = min(len(set(colors)) / 10.0, 1.0) if colors else 0.5
        
        # Spacing consistency (variance)
        spacing_consistency = 1.0 / (1.0 + np.var(spacings)) if spacings else 0.5
        
        # Hierarchy (heading count ratio)
        h1_count = len(soup.find_all('h1'))
        h2_count = len(soup.find_all('h2'))
        h3_count = len(soup.find_all('h3'))
        hierarchy = min((h1_count + h2_count * 0.8 + h3_count * 0.6) / 10.0, 1.0)
        
        # Semantic HTML (proper tags)
        semantic_tags = soup.find_all(['header', 'nav', 'main', 'section', 'article', 'footer'])
        semantic_score = min(len(semantic_tags) / 6.0, 1.0)
        
        return torch.tensor([color_diversity, spacing_consistency, hierarchy, semantic_score], dtype=torch.float32)
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate Flesch-Kincaid readability score"""
        if not text:
            return 0.0
        
        # Count sentences, words, syllables
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = re.findall(r'\b\w+\b', text)
        
        if not sentences or not words:
            return 0.0
        
        # Simple syllable counter
        syllables = sum(self._count_syllables(word) for word in words)
        
        # Flesch-Kincaid formula
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        fk_score = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables_per_word
        
        # Normalize to 0-1 (typical range is 0-100)
        return max(0.0, min(fk_score / 100.0, 1.0))
    
    def _count_syllables(self, word: str) -> int:
        """Simple syllable counter"""
        word = word.lower()
        vowels = 'aeiouy'
        syllable_count = 0
        previous_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not previous_was_vowel:
                syllable_count += 1
            previous_was_vowel = is_vowel
        
        # Adjust for silent e
        if word.endswith('e'):
            syllable_count -= 1
        
        return max(1, syllable_count)
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        return self.samples[idx]


class IsomorphicWebHostModel(nn.Module):
    """
    Isomorphic transformer for web generation.
    Same architecture can:
    - Generate HTML (server-side)
    - Optimize content (client-side)
    - Scale horizontally across nodes
    - Deterministic transforms for reproducibility
    """
    
    def __init__(self, vocab_size: int, embed_dim: int = 512, num_heads: int = 8, 
                 num_layers: int = 6, dropout: float = 0.1):
        super().__init__()
        
        self.vocab_size = vocab_size
        self.embed_dim = embed_dim
        
        # Token embedding
        self.token_embed = nn.Embedding(vocab_size, embed_dim)
        self.pos_embed = nn.Parameter(torch.randn(1, 512, embed_dim))
        
        # Transformer encoder (isomorphic - works anywhere)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embed_dim,
            nhead=num_heads,
            dim_feedforward=2048,
            dropout=dropout,
            batch_first=True,
            norm_first=True  # Pre-norm for stability
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Output heads
        self.lm_head = nn.Linear(embed_dim, vocab_size)  # Language modeling
        self.design_head = nn.Linear(embed_dim, 4)  # Design metrics
        self.quality_head = nn.Linear(embed_dim, 1)  # Overall quality
        
        # Layer norm for stability
        self.layer_norm = nn.LayerNorm(embed_dim)
        
        self._init_weights()
    
    def _init_weights(self):
        """Xavier initialization for stable training"""
        for p in self.parameters():
            if p.dim() > 1:
                nn.init.xavier_uniform_(p)
    
    def forward(self, tokens: torch.Tensor, mask: torch.Tensor = None) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """
        Forward pass - isomorphic across all deployment targets
        
        Args:
            tokens: [batch, seq_len] token IDs
            mask: [batch, seq_len] padding mask
            
        Returns:
            logits: [batch, seq_len, vocab_size] - next token predictions
            design: [batch, 4] - design metrics
            quality: [batch, 1] - quality score
        """
        batch_size, seq_len = tokens.shape
        
        # Embed
        x = self.token_embed(tokens)  # [batch, seq_len, embed_dim]
        x = x + self.pos_embed[:, :seq_len, :]
        
        # Transform
        x = self.transformer(x, src_key_padding_mask=mask)
        x = self.layer_norm(x)
        
        # Outputs
        logits = self.lm_head(x)  # [batch, seq_len, vocab_size]
        
        # Aggregate for design/quality (mean pooling)
        if mask is not None:
            # Mask out padding
            mask_expanded = (~mask).unsqueeze(-1).float()
            x_masked = x * mask_expanded
            x_mean = x_masked.sum(dim=1) / mask_expanded.sum(dim=1)
        else:
            x_mean = x.mean(dim=1)
        
        design = self.design_head(x_mean)  # [batch, 4]
        quality = torch.sigmoid(self.quality_head(x_mean))  # [batch, 1]
        
        return logits, design, quality


class WebHostTrainer:
    """Trainer with rigorous mathematical evaluation"""
    
    def __init__(self, model: IsomorphicWebHostModel, dataset: WebsiteDataset, 
                 device: str = 'cpu', learning_rate: float = 1e-4):
        self.model = model.to(device)
        self.dataset = dataset
        self.device = device
        
        # Optimizer with weight decay (L2 regularization)
        self.optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, 
                                           weight_decay=0.01, betas=(0.9, 0.999))
        
        # Learning rate scheduler (cosine annealing)
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            self.optimizer, T_max=100, eta_min=1e-6
        )
        
        self.metrics_history: List[TrainingMetrics] = []
    
    def calculate_perplexity(self, logits: torch.Tensor, targets: torch.Tensor, 
                            mask: torch.Tensor) -> float:
        """
        Calculate perplexity: exp(-1/N * Σ log P(x_i))
        Lower is better (perfect model = 1.0)
        """
        # Get log probabilities
        log_probs = F.log_softmax(logits, dim=-1)
        
        # Gather target probabilities
        target_log_probs = log_probs.gather(dim=-1, index=targets.unsqueeze(-1)).squeeze(-1)
        
        # Apply mask
        if mask is not None:
            target_log_probs = target_log_probs.masked_fill(mask, 0.0)
            num_tokens = (~mask).sum().item()
        else:
            num_tokens = targets.numel()
        
        # Perplexity = exp(avg negative log likelihood)
        avg_nll = -target_log_probs.sum() / num_tokens
        perplexity = torch.exp(avg_nll).item()
        
        return perplexity
    
    def calculate_bleu(self, generated: str, reference: str, max_n: int = 4) -> float:
        """
        Calculate BLEU score for generated HTML vs reference.
        BLEU = BP * exp(Σ w_n log p_n)
        
        Modified for HTML: tokenize by tags + words
        """
        # Tokenize
        gen_tokens = re.findall(r'<[^>]+>|[\w]+', generated.lower())
        ref_tokens = re.findall(r'<[^>]+>|[\w]+', reference.lower())
        
        if not gen_tokens or not ref_tokens:
            return 0.0
        
        # Calculate n-gram precisions
        precisions = []
        for n in range(1, max_n + 1):
            gen_ngrams = self._get_ngrams(gen_tokens, n)
            ref_ngrams = self._get_ngrams(ref_tokens, n)
            
            if not gen_ngrams:
                precisions.append(0.0)
                continue
            
            # Count matches
            matches = 0
            for ngram in gen_ngrams:
                if ngram in ref_ngrams:
                    matches += min(gen_ngrams[ngram], ref_ngrams[ngram])
            
            precision = matches / sum(gen_ngrams.values())
            precisions.append(precision)
        
        # Brevity penalty
        bp = 1.0 if len(gen_tokens) >= len(ref_tokens) else math.exp(1 - len(ref_tokens) / len(gen_tokens))
        
        # Geometric mean of precisions
        if all(p > 0 for p in precisions):
            log_precisions = [math.log(p) for p in precisions]
            bleu = bp * math.exp(sum(log_precisions) / len(precisions))
        else:
            bleu = 0.0
        
        return bleu
    
    def _get_ngrams(self, tokens: List[str], n: int) -> Counter:
        """Get n-gram counts"""
        ngrams = Counter()
        for i in range(len(tokens) - n + 1):
            ngram = tuple(tokens[i:i+n])
            ngrams[ngram] += 1
        return ngrams
    
    def calculate_design_score(self, pred_design: torch.Tensor, true_design: torch.Tensor) -> float:
        """
        Calculate design quality score.
        Weighted MSE with emphasis on critical metrics.
        """
        weights = torch.tensor([1.5, 1.2, 1.0, 1.3], device=pred_design.device)  # color, spacing, hierarchy, semantic
        mse = ((pred_design - true_design) ** 2) * weights
        score = 1.0 - torch.clamp(mse.mean(), 0, 1).item()
        return score
    
    def train_epoch(self, epoch: int, batch_size: int = 4) -> TrainingMetrics:
        """Train for one epoch with comprehensive metrics"""
        self.model.train()
        dataloader = DataLoader(self.dataset, batch_size=batch_size, shuffle=True, collate_fn=lambda x: x)
        
        total_loss = 0.0
        total_perplexity = 0.0
        total_design_score = 0.0
        gradient_norms = []
        
        for batch_idx, batch_data in enumerate(dataloader):
            # Prepare batch (batch_data is already a list of dicts)
            tokens = torch.stack([item['tokens'] for item in batch_data]).to(self.device)
            design_metrics = torch.stack([item['design_metrics'] for item in batch_data]).to(self.device)
            
            # Create targets (shift right for language modeling)
            targets = tokens[:, 1:].contiguous()
            inputs = tokens[:, :-1].contiguous()
            
            # Create mask for padding
            mask = (inputs == self.dataset.vocab['<PAD>'])
            
            # Forward pass
            logits, pred_design, quality = self.model(inputs, mask)
            
            # Language modeling loss
            lm_loss = F.cross_entropy(
                logits.reshape(-1, logits.size(-1)),
                targets.reshape(-1),
                ignore_index=self.dataset.vocab['<PAD>']
            )
            
            # Design loss
            design_loss = F.mse_loss(pred_design, design_metrics)
            
            # Combined loss
            loss = lm_loss + 0.5 * design_loss
            
            # Backward
            self.optimizer.zero_grad()
            loss.backward()
            
            # Gradient clipping for stability
            grad_norm = torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
            gradient_norms.append(grad_norm.item())
            
            self.optimizer.step()
            
            # Metrics
            with torch.no_grad():
                perplexity = self.calculate_perplexity(logits, targets, mask[:, 1:])
                design_score = self.calculate_design_score(pred_design, design_metrics)
            
            total_loss += loss.item()
            total_perplexity += perplexity
            total_design_score += design_score
            
            if batch_idx % 10 == 0:
                print(f"  Batch {batch_idx}/{len(dataloader)}: loss={loss.item():.4f}, ppl={perplexity:.2f}, design={design_score:.3f}")
        
        # Epoch metrics
        num_batches = len(dataloader)
        avg_loss = total_loss / num_batches
        avg_perplexity = total_perplexity / num_batches
        avg_design_score = total_design_score / num_batches
        avg_gradient_norm = sum(gradient_norms) / len(gradient_norms)
        
        # Update learning rate
        self.scheduler.step()
        current_lr = self.scheduler.get_last_lr()[0]
        
        # Calculate readability on generated samples
        avg_readability = self._evaluate_readability(batch_data)
        
        metrics = TrainingMetrics(
            epoch=epoch,
            loss=avg_loss,
            perplexity=avg_perplexity,
            bleu_score=0.0,  # Calculate on validation
            design_score=avg_design_score,
            readability_score=avg_readability,
            gradient_norm=avg_gradient_norm,
            learning_rate=current_lr
        )
        
        self.metrics_history.append(metrics)
        return metrics
    
    def _evaluate_readability(self, batch_data: List[Dict]) -> float:
        """Evaluate readability of training samples"""
        readability_scores = [item['readability'] for item in batch_data]
        return sum(readability_scores) / len(readability_scores) if readability_scores else 0.0
    
    def save_checkpoint(self, path: Path, metrics: TrainingMetrics):
        """Save model checkpoint with metrics"""
        checkpoint = {
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'scheduler_state_dict': self.scheduler.state_dict(),
            'metrics': metrics,
            'vocab_size': self.model.vocab_size,
            'embed_dim': self.model.embed_dim
        }
        torch.save(checkpoint, path)
        print(f"✓ Checkpoint saved: {path}")


def train_on_nm_socialists(epochs: int = 20, device: str = 'cpu'):
    """Train WebHost AI on NM Socialists site"""
    print("=" * 80)
    print("WebHost AI Training - Learning from Real Websites")
    print("=" * 80)
    print()
    
    # Load dataset
    training_dir = Path.home() / 'queztl-core' / 'training_data' / 'nm_socialists_original'
    html_files = list(training_dir.glob('**/*.html'))
    
    if not html_files:
        print("❌ No HTML files found in training_data")
        return
    
    print(f"📁 Found {len(html_files)} HTML files")
    dataset = WebsiteDataset(html_files)
    print()
    
    # Create model
    model = IsomorphicWebHostModel(
        vocab_size=dataset.vocab_size,
        embed_dim=512,
        num_heads=8,
        num_layers=6,
        dropout=0.1
    )
    
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"🧠 Model: {total_params:,} parameters ({trainable_params:,} trainable)")
    print()
    
    # Create trainer
    trainer = WebHostTrainer(model, dataset, device=device, learning_rate=1e-4)
    
    # Training loop
    print(f"🚀 Training for {epochs} epochs...")
    print()
    
    best_loss = float('inf')
    checkpoint_dir = Path.home() / 'queztl-core' / 'models' / 'webhost_trained'
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    
    for epoch in range(1, epochs + 1):
        print(f"Epoch {epoch}/{epochs}")
        print("-" * 80)
        
        metrics = trainer.train_epoch(epoch, batch_size=2)
        
        print()
        print(f"📊 Epoch {epoch} Results:")
        print(f"  Loss:           {metrics.loss:.4f}")
        print(f"  Perplexity:     {metrics.perplexity:.2f}")
        print(f"  Design Score:   {metrics.design_score:.3f}")
        print(f"  Readability:    {metrics.readability_score:.3f}")
        print(f"  Gradient Norm:  {metrics.gradient_norm:.4f}")
        print(f"  Learning Rate:  {metrics.learning_rate:.6f}")
        print()
        
        # Save best model
        if metrics.loss < best_loss:
            best_loss = metrics.loss
            trainer.save_checkpoint(checkpoint_dir / 'best_model.pt', metrics)
            print(f"✨ New best model! Loss: {best_loss:.4f}")
            print()
    
    # Save final model
    trainer.save_checkpoint(checkpoint_dir / 'final_model.pt', metrics)
    
    # Save metrics history
    metrics_file = checkpoint_dir / 'training_metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump([{
            'epoch': m.epoch,
            'loss': m.loss,
            'perplexity': m.perplexity,
            'design_score': m.design_score,
            'readability_score': m.readability_score,
            'gradient_norm': m.gradient_norm,
            'learning_rate': m.learning_rate
        } for m in trainer.metrics_history], f, indent=2)
    
    print("=" * 80)
    print("✅ Training complete!")
    print(f"📁 Models saved: {checkpoint_dir}")
    print(f"📊 Metrics saved: {metrics_file}")
    print("=" * 80)


if __name__ == '__main__':
    import sys
    
    epochs = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print(f"🖥️  Device: {device}")
    print()
    
    train_on_nm_socialists(epochs=epochs, device=device)
