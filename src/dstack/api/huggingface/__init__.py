from typing import Dict, Optional

from dstack.api._public.huggingface.finetuning.sft import FineTuningTask


class SFTFineTuningTask(FineTuningTask):
    def __init__(
        self,
        model_name: str,
        dataset_name: str,
        env: Dict[str, str],
        new_model_name: Optional[str] = None,
        report_to: Optional[str] = None,
        per_device_train_batch_size: int = 4,
        per_device_eval_batch_size: int = 4,
        gradient_accumulation_steps: int = 1,
        learning_rate: float = 2e-4,
        max_grad_norm: float = 0.3,
        weight_decay: float = 0.001,
        lora_alpha: int = 16,
        lora_dropout: float = 0.1,
        lora_r: int = 64,
        max_seq_length: Optional[int] = None,
        use_4bit: bool = True,
        use_nested_quant: bool = True,
        bnb_4bit_compute_dtype: str = "float16",
        bnb_4bit_quant_type: str = "nf4",
        num_train_epochs: float = 1,
        fp16: bool = False,
        bf16: bool = False,
        packing: bool = False,
        gradient_checkpointing: bool = True,
        optim: str = "paged_adamw_32bit",
        lr_scheduler_type: str = "constant",
        max_steps: int = -1,
        warmup_ratio: float = 0.03,
        group_by_length: bool = True,
        save_steps: int = 0,
        logging_steps: int = 25,
    ):
        super().__init__(
            model_name,
            dataset_name,
            new_model_name,
            env,
            report_to,
            per_device_train_batch_size,
            per_device_eval_batch_size,
            gradient_accumulation_steps,
            learning_rate,
            max_grad_norm,
            weight_decay,
            lora_alpha,
            lora_dropout,
            lora_r,
            max_seq_length,
            use_4bit,
            use_nested_quant,
            bnb_4bit_compute_dtype,
            bnb_4bit_quant_type,
            num_train_epochs,
            fp16,
            bf16,
            packing,
            gradient_checkpointing,
            optim,
            lr_scheduler_type,
            max_steps,
            warmup_ratio,
            group_by_length,
            save_steps,
            logging_steps,
        )