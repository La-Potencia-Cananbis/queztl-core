#!/usr/bin/env python3
"""
Theory Training Pipeline
Train AI models on communist theory corpus
"""

import os
import json
import torch
from pathlib import Path
from typing import List, Dict
from transformers import (
    GPT2LMHeadModel, GPT2Tokenizer,
    AutoTokenizer, AutoModelForCausalLM,
    TrainingArguments, Trainer, DataCollatorForLanguageModeling
)
from datasets import Dataset

class TheoryTrainer:
    """Train models on communist theory"""
    
    def __init__(self, library_path: str = "data/theory_library"):
        self.library_path = Path(library_path)
        self.texts_dir = self.library_path / "texts"
        self.models_dir = Path("models/theory_models")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
    def load_corpus(self) -> List[str]:
        """Load all theory texts"""
        texts = []
        for filepath in self.texts_dir.glob("*.txt"):
            content = filepath.read_text()
            texts.append(content)
        return texts
    
    def prepare_dataset(self, texts: List[str], tokenizer) -> Dataset:
        """Tokenize texts for training"""
        # Concatenate all texts
        full_text = "\n\n".join(texts)
        
        # Tokenize
        encodings = tokenizer(full_text, truncation=True, max_length=512)
        
        # Create dataset
        dataset = Dataset.from_dict({
            "input_ids": [encodings["input_ids"]]
        })
        
        return dataset
    
    def train_gpt2(self, epochs: int = 3):
        """Train GPT-2 on theory corpus"""
        print("🧠 Training GPT-2 on Communist Theory")
        print("=" * 60)
        
        # Load model and tokenizer
        model_name = "gpt2"
        tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        tokenizer.pad_token = tokenizer.eos_token
        model = GPT2LMHeadModel.from_pretrained(model_name)
        
        # Load corpus
        texts = self.load_corpus()
        print(f"✓ Loaded {len(texts)} texts")
        
        # Prepare dataset
        dataset = self.prepare_dataset(texts, tokenizer)
        print(f"✓ Dataset prepared")
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=str(self.models_dir / "gpt2_theory"),
            num_train_epochs=epochs,
            per_device_train_batch_size=2,
            save_steps=100,
            save_total_limit=2,
            logging_steps=10,
        )
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset,
            data_collator=data_collator,
        )
        
        # Train
        print("🔥 Training started...")
        trainer.train()
        
        # Save
        output_path = self.models_dir / "gpt2_theory_final"
        trainer.save_model(str(output_path))
        tokenizer.save_pretrained(str(output_path))
        
        print(f"✓ Model saved: {output_path}")
        
        return output_path
    
    def generate_study_guide(self, topic: str, model_path: Path) -> str:
        """Generate study guide using trained model"""
        tokenizer = GPT2Tokenizer.from_pretrained(str(model_path))
        model = GPT2LMHeadModel.from_pretrained(str(model_path))
        
        prompt = f"Study guide on {topic}:\n\n"
        inputs = tokenizer(prompt, return_tensors="pt")
        
        outputs = model.generate(
            inputs["input_ids"],
            max_length=300,
            num_return_sequences=1,
            temperature=0.8,
            do_sample=True
        )
        
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return text

def main():
    trainer = TheoryTrainer()
    
    # Train GPT-2
    model_path = trainer.train_gpt2(epochs=2)
    
    # Generate study guides
    topics = ["surplus value", "class struggle", "imperialism"]
    print("\n📚 Generating Study Guides:")
    print("=" * 60)
    
    for topic in topics:
        guide = trainer.generate_study_guide(topic, model_path)
        print(f"\n{topic.upper()}:")
        print(guide[:200] + "...")

if __name__ == "__main__":
    main()
