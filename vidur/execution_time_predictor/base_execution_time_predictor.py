from abc import ABC, abstractmethod

from vidur.config import BaseExecutionTimePredictorConfig
from vidur.config.model_config import BaseModelConfig
from vidur.entities import Batch, ExecutionTime


class BaseExecutionTimePredictor(ABC):
    def __init__(self, config: BaseExecutionTimePredictorConfig, model_config: BaseModelConfig) -> None:
        self._config = config
        self._model_config = model_config

    def get_execution_time(self, batch: Batch, pipeline_stage: int) -> ExecutionTime:
        if pipeline_stage == self._config.num_pipeline_stages - 1:
            pipeline_parallel_communication_time = 0
        else:
            pipeline_parallel_communication_time = (
                self._get_pipeline_parallel_communication_time(batch)
            )

        if self._config.num_tensor_parallel_workers == 1:
            tensor_parallel_communication_time = 0
        else:
            tensor_parallel_communication_time = (
                self._get_tensor_parallel_communication_time(batch)
            )

        return ExecutionTime(
            self._config.num_layers_per_pipeline_stage,
            self._get_attention_rope_execution_time(batch),
            self._get_attention_kv_cache_save_execution_time(batch),
            self._get_attention_decode_execution_time(batch),
            self._get_attention_prefill_execution_time(batch),
            self._get_attention_layer_pre_proj_execution_time(batch),
            self._get_attention_layer_post_proj_execution_time(batch),
            self._get_mlp_layer_up_proj_execution_time(batch),
            self._get_mlp_layer_down_proj_execution_time(batch),
            self._get_mlp_layer_act_execution_time(batch),
            self._get_attn_norm_layer_act_execution_time(batch),
            self._get_mlp_norm_layer_act_execution_time(batch),
            self._get_add_layer_act_execution_time(batch),
            tensor_parallel_communication_time,
            pipeline_parallel_communication_time,
            self._get_schedule_time(batch),
            self._get_sampler_e2e_time(batch),
            self._get_prepare_inputs_e2e_time(batch),
            self._get_process_model_outputs_time(batch),
            self._get_ray_comm_time(batch),
        )

    @abstractmethod
    def _get_attention_layer_pre_proj_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_attention_layer_post_proj_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_attention_rope_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_attention_kv_cache_save_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_attention_decode_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_attention_prefill_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_mlp_layer_up_proj_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_mlp_layer_down_proj_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_mlp_layer_act_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_tensor_parallel_communication_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_pipeline_parallel_communication_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_schedule_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_sampler_e2e_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_prepare_inputs_e2e_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_process_model_outputs_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_ray_comm_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_mlp_norm_layer_act_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_attn_norm_layer_act_execution_time(self, batch: Batch) -> float:
        pass

    @abstractmethod
    def _get_add_layer_act_execution_time(self, batch: Batch) -> float:
        pass
