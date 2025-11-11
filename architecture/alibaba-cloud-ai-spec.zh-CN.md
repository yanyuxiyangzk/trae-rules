---
trigger: manual
---

# 阿里云 AI 卓越架构规范 v1.0
# ============================================
# AI 辅助开发的阿里云 AI 应用架构标准
# 通过将 [ENABLED] 更改为 [DISABLED] 来启用/禁用规则
#
# 使用方法：
# 1. 将此文件放在项目根目录
# 2. 根据项目需求启用/禁用规则
# 3. 在 AI 对话中使用 @alibaba-cloud-ai-spec.zh-CN.txt 引用
# 4. AI 将只遵循 ENABLED 的规则
#
# 参考文档：阿里云 AI 卓越架构框架、云原生最佳实践
# 依赖规范：requirements-spec.txt、security-spec.txt、deployment-spec.txt
# 最后更新：2025-11-10
# ============================================

## [规则 1] 模型服务化架构 [ENABLED]
# AI 模型作为微服务部署

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 使用阿里云 PAI（Platform for AI）部署模型
- 模型服务独立于业务逻辑
- 支持模型版本管理和灰度发布
- 实施模型 A/B 测试能力
- 使用容器化部署（ECI/ACK）

后果：
- 模型与业务耦合导致升级困难
- 无版本管理导致无法回滚

示例（Flask 模型服务）：
```python
from flask import Flask, request, jsonify
from alibabacloud_pai_dsw20220101 import models as pai_models
import oss2
import logging

app = Flask(__name__)

class ModelService:
    def __init__(self):
        self.model = None
        self.model_version = None
        
    def load_model_from_oss(self, bucket_name, model_path):
        """从 OSS 加载模型"""
        auth = oss2.Auth('<AccessKeyId>', '<AccessKeySecret>')
        bucket = oss2.Bucket(auth, 'oss-cn-hangzhou.aliyuncs.com', bucket_name)
        
        # 下载模型文件
        bucket.get_object_to_file(model_path, 'local_model.pkl')
        
        # 加载模型
        import pickle
        with open('local_model.pkl', 'rb') as f:
            self.model = pickle.load(f)
        
        self.model_version = model_path.split('/')[-1]
        logging.info(f"模型已加载: {self.model_version}")
    
    def predict(self, features):
        """模型推理"""
        if self.model is None:
            raise ValueError("模型未加载")
        
        return self.model.predict(features)

model_service = ModelService()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_version': model_service.model_version,
        'model_loaded': model_service.model is not None
    })

@app.route('/v1/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        features = data.get('features')
        
        if not features:
            return jsonify({'error': 'Missing features'}), 400
        
        prediction = model_service.predict(features)
        
        return jsonify({
            'prediction': prediction.tolist(),
            'model_version': model_service.model_version
        })
    except Exception as e:
        logging.error(f"预测错误: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # 从 OSS 加载模型
    model_service.load_model_from_oss(
        bucket_name='ai-models',
        model_path='models/v1.2.0/model.pkl'
    )
    app.run(host='0.0.0.0', port=8080)
```

WHY: 模型服务化实现模型与业务解耦，支持独立扩展和版本管理


## [规则 2] 向量检索与存储 [ENABLED]
# 使用阿里云向量检索服务

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 使用 Hologres 或 AnalyticDB 进行向量存储
- 集成阿里云 DashVector 进行高性能检索
- 实施向量索引优化（HNSW, IVF）
- 支持混合检索（向量 + 关键词）
- 实施向量数据备份和恢复

示例（DashVector 集成）：
```python
from dashvector import Client, Doc
from typing import List, Dict
import numpy as np

class VectorStore:
    def __init__(self, api_key: str, endpoint: str):
        self.client = Client(api_key=api_key, endpoint=endpoint)
        self.collection = None
    
    def create_collection(self, name: str, dimension: int):
        """创建向量集合"""
        self.collection = self.client.create_collection(
            name=name,
            dimension=dimension,
            metric='cosine',  # 余弦相似度
            fields_schema={
                'content': str,
                'metadata': dict
            }
        )
        return self.collection
    
    def insert_vectors(self, vectors: List[np.ndarray], 
                       contents: List[str],
                       metadatas: List[Dict]):
        """批量插入向量"""
        docs = [
            Doc(
                id=str(i),
                vector=vec.tolist(),
                fields={
                    'content': content,
                    'metadata': metadata
                }
            )
            for i, (vec, content, metadata) in 
            enumerate(zip(vectors, contents, metadatas))
        ]
        
        result = self.collection.upsert(docs)
        return result
    
    def search(self, query_vector: np.ndarray, 
               top_k: int = 10,
               filters: Dict = None):
        """向量检索"""
        result = self.collection.query(
            vector=query_vector.tolist(),
            topk=top_k,
            filter=filters,
            include_vector=False
        )
        
        return [{
            'id': doc.id,
            'score': doc.score,
            'content': doc.fields.get('content'),
            'metadata': doc.fields.get('metadata')
        } for doc in result]

# 使用示例
vector_store = VectorStore(
    api_key='your-dashvector-api-key',
    endpoint='https://dashvector.cn-hangzhou.aliyuncs.com'
)

# 创建集合
collection = vector_store.create_collection(
    name='knowledge_base',
    dimension=768  # BERT 向量维度
)

# 插入向量数据
embeddings = generate_embeddings(texts)  # 生成向量
vector_store.insert_vectors(
    vectors=embeddings,
    contents=texts,
    metadatas=[{'source': 'doc1'} for _ in texts]
)

# 检索
query_embedding = generate_embeddings(['用户查询'])[0]
results = vector_store.search(query_embedding, top_k=5)
```


## [规则 3] 大模型调用与管理 [ENABLED]
# 集成阿里云通义大模型

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 使用阿里云百炼平台（DashScope）调用通义千问
- 实施 Prompt 工程最佳实践
- 实现流式输出和批量处理
- 实施 Token 使用监控和成本控制
- 使用 Function Calling 能力

后果：
- 不当的 Prompt 导致输出质量差
- 缺少流控导致成本失控

示例（通义千问集成）：
```python
from http import HTTPStatus
import dashscope
from dashscope import Generation
import json

class QwenService:
    def __init__(self, api_key: str):
        dashscope.api_key = api_key
        self.model = 'qwen-turbo'
        self.max_tokens = 1500
        self.temperature = 0.7
    
    def chat(self, messages: list, stream: bool = False):
        """对话生成"""
        response = Generation.call(
            model=self.model,
            messages=messages,
            result_format='message',
            stream=stream,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=0.8
        )
        
        if stream:
            return self._handle_stream(response)
        else:
            if response.status_code == HTTPStatus.OK:
                return response.output.choices[0].message.content
            else:
                raise Exception(f"API 调用失败: {response.message}")
    
    def _handle_stream(self, response):
        """处理流式响应"""
        full_content = []
        for chunk in response:
            if chunk.status_code == HTTPStatus.OK:
                content = chunk.output.choices[0].message.content
                full_content.append(content)
                yield content
            else:
                raise Exception(f"流式调用失败: {chunk.message}")
    
    def function_calling(self, messages: list, functions: list):
        """Function Calling"""
        response = Generation.call(
            model='qwen-plus',
            messages=messages,
            functions=functions,
            result_format='message'
        )
        
        if response.status_code == HTTPStatus.OK:
            choice = response.output.choices[0]
            if choice.message.get('function_call'):
                return {
                    'type': 'function_call',
                    'function': choice.message.function_call.name,
                    'arguments': json.loads(choice.message.function_call.arguments)
                }
            else:
                return {
                    'type': 'text',
                    'content': choice.message.content
                }
        else:
            raise Exception(f"Function calling 失败: {response.message}")
    
    def token_usage_monitor(self, response):
        """Token 使用监控"""
        usage = response.usage
        return {
            'input_tokens': usage.input_tokens,
            'output_tokens': usage.output_tokens,
            'total_tokens': usage.total_tokens
        }

# 使用示例
qwen = QwenService(api_key='your-dashscope-api-key')

# 普通对话
messages = [
    {'role': 'system', 'content': '你是一个专业的AI助手'},
    {'role': 'user', 'content': '请解释什么是向量数据库？'}
]
response = qwen.chat(messages)

# 流式对话
for chunk in qwen.chat(messages, stream=True):
    print(chunk, end='', flush=True)

# Function Calling
functions = [{
    'name': 'get_weather',
    'description': '获取指定城市的天气信息',
    'parameters': {
        'type': 'object',
        'properties': {
            'city': {'type': 'string', 'description': '城市名称'}
        },
        'required': ['city']
    }
}]

result = qwen.function_calling(
    messages=[{'role': 'user', 'content': '杭州今天天气怎么样？'}],
    functions=functions
)
```


## [规则 4] 数据湖与特征工程 [ENABLED]
# 使用阿里云数据湖分析

STATUS: ENABLED
说明：
- 使用 OSS 作为数据湖存储
- 使用 MaxCompute 进行大规模数据处理
- 集成 PAI-Feature Store 管理特征
- 实施数据版本管理
- 实现离线/在线特征一致性

示例（PAI Feature Store）：
```python
from pai.feature_store import FeatureStore, FeatureView
from pai.common.oss_utils import OSSDataSource
import pandas as pd

class FeatureManager:
    def __init__(self, project_name: str):
        self.fs = FeatureStore(project_name=project_name)
    
    def create_feature_view(self, name: str, features: list):
        """创建特征视图"""
        feature_view = FeatureView(
            name=name,
            features=features,
            source=OSSDataSource(
                path='oss://bucket/features/',
                format='parquet'
            )
        )
        
        self.fs.create_feature_view(feature_view)
        return feature_view
    
    def get_online_features(self, feature_view_name: str, 
                           entity_keys: list):
        """获取在线特征"""
        feature_view = self.fs.get_feature_view(feature_view_name)
        
        features = feature_view.get_online_features(
            entity_keys=entity_keys
        )
        
        return features
    
    def write_features(self, feature_view_name: str, 
                       features_df: pd.DataFrame):
        """写入特征数据"""
        feature_view = self.fs.get_feature_view(feature_view_name)
        
        # 写入离线存储（OSS）
        feature_view.write_features(
            features_df,
            mode='append'
        )
        
        # 同步到在线存储（Hologres/Redis）
        feature_view.publish_to_online()

# 使用示例
fm = FeatureManager(project_name='ai_project')

# 创建特征视图
features = [
    {'name': 'user_age', 'type': 'int'},
    {'name': 'user_gender', 'type': 'string'},
    {'name': 'purchase_count_7d', 'type': 'int'},
    {'name': 'avg_order_value_30d', 'type': 'float'}
]
fm.create_feature_view(name='user_features', features=features)

# 获取在线特征用于实时推理
features = fm.get_online_features(
    feature_view_name='user_features',
    entity_keys=['user_123', 'user_456']
)
```


## [规则 5] 模型训练与优化 [ENABLED]
# 使用阿里云 PAI 进行模型训练

STATUS: ENABLED
说明：
- 使用 PAI-DLC 进行分布式训练
- 实施自动超参数调优（AutoML）
- 使用混合精度训练加速
- 实施模型压缩和量化
- 使用 GPU/NPU 加速训练

示例（PAI-DLC 训练任务）：
```python
from alibabacloud_pai_dlc20201203 import models as dlc_models
from alibabacloud_pai_dlc20201203.client import Client as DLCClient
from alibabacloud_tea_openapi.models import Config

class TrainingJobManager:
    def __init__(self, access_key_id: str, access_key_secret: str):
        config = Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint='pai-dlc.cn-hangzhou.aliyuncs.com'
        )
        self.client = DLCClient(config)
    
    def create_training_job(self, job_config: dict):
        """创建训练任务"""
        request = dlc_models.CreateJobRequest(
            display_name=job_config['name'],
            job_type='PyTorchJob',
            job_specs=[
                dlc_models.JobSpec(
                    type='Worker',
                    replicas=job_config.get('workers', 1),
                    image=job_config['image'],
                    resource_config=dlc_models.ResourceConfig(
                        cpu=job_config.get('cpu', '8'),
                        memory=job_config.get('memory', '32Gi'),
                        gpu=job_config.get('gpu', '1'),
                        gpu_type=job_config.get('gpu_type', 'V100')
                    )
                )
            ],
            code_source=dlc_models.CodeSource(
                code_source_type='OSS',
                location=job_config['code_path']
            ),
            data_sources=[
                dlc_models.DataSource(
                    data_source_type='OSS',
                    location=job_config['data_path']
                )
            ],
            user_command=job_config['command']
        )
        
        response = self.client.create_job(request)
        return response.body.job_id
    
    def monitor_job(self, job_id: str):
        """监控训练任务"""
        request = dlc_models.GetJobRequest(job_id=job_id)
        response = self.client.get_job(request)
        
        return {
            'status': response.body.status,
            'duration': response.body.duration,
            'metrics': response.body.job_metrics
        }

# 使用示例
trainer = TrainingJobManager(
    access_key_id='your-access-key',
    access_key_secret='your-secret-key'
)

job_config = {
    'name': 'bert-finetuning',
    'image': 'registry.cn-hangzhou.aliyuncs.com/pai-dlc/pytorch:1.12',
    'workers': 4,
    'gpu': 2,
    'gpu_type': 'V100',
    'code_path': 'oss://bucket/code/train.py',
    'data_path': 'oss://bucket/data/train_data/',
    'command': 'python train.py --epochs 10 --batch-size 32'
}

job_id = trainer.create_training_job(job_config)
print(f"训练任务已创建: {job_id}")
```


## [规则 6] 实时推理服务 [ENABLED]
# 高性能在线推理部署

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 使用 PAI-EAS 部署推理服务
- 实施模型自动扩缩容
- 使用模型推理加速（TensorRT, ONNX）
- 实施请求批处理（Batching）
- 监控推理延迟和吞吐量

后果：
- 推理延迟过高导致用户体验差
- 缺少弹性伸缩导致成本浪费

示例（PAI-EAS 部署）：
```python
from alibabacloud_paielasticdatasetaccelerator20220801.client import Client
from alibabacloud_tea_openapi.models import Config
import json

class InferenceService:
    def __init__(self, access_key_id: str, access_key_secret: str):
        config = Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint='pai-eas.cn-hangzhou.aliyuncs.com'
        )
        self.client = Client(config)
    
    def deploy_service(self, service_config: dict):
        """部署推理服务"""
        config_json = {
            'name': service_config['name'],
            'model_path': service_config['model_path'],
            'processor': service_config.get('processor', 'tensorflow'),
            'metadata': {
                'instance': service_config.get('instance', 1),
                'cpu': service_config.get('cpu', 4),
                'memory': service_config.get('memory', 8000),
                'gpu': service_config.get('gpu', 0)
            },
            'features': {
                'eas.autoscaler.min_instance': 1,
                'eas.autoscaler.max_instance': 10,
                'eas.autoscaler.metric': 'qps',
                'eas.autoscaler.threshold': 100
            }
        }
        
        # 部署服务
        # 实际调用 PAI-EAS API
        service_name = service_config['name']
        return f"服务已部署: {service_name}"
    
    def predict(self, service_url: str, token: str, data: dict):
        """调用推理服务"""
        import requests
        
        headers = {
            'Authorization': token,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            service_url,
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"推理失败: {response.text}")

# 使用示例
inference = InferenceService(
    access_key_id='your-key',
    access_key_secret='your-secret'
)

# 部署服务
service_config = {
    'name': 'text-classification-service',
    'model_path': 'oss://bucket/models/bert_model/',
    'processor': 'pytorch',
    'instance': 2,
    'cpu': 8,
    'memory': 16000,
    'gpu': 1
}
inference.deploy_service(service_config)

# 调用推理
result = inference.predict(
    service_url='http://xxx.pai-eas.aliyuncs.com/api/predict/text-classification',
    token='your-service-token',
    data={'text': '这是一个测试文本'}
)
```


## [规则 7] 监控与可观测性 [ENABLED]
# 全链路监控和日志

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 使用阿里云 SLS（日志服务）采集日志
- 集成 ARMS（应用实时监控）
- 监控模型指标（准确率、延迟、吞吐量）
- 实施分布式追踪（Tracing）
- 配置告警规则

示例（SLS 集成）：
```python
from aliyun.log import LogClient, PutLogsRequest, LogItem
import time
import json

class AIMonitor:
    def __init__(self, endpoint: str, access_key_id: str, 
                 access_key_secret: str, project: str, logstore: str):
        self.client = LogClient(endpoint, access_key_id, access_key_secret)
        self.project = project
        self.logstore = logstore
    
    def log_prediction(self, model_name: str, input_data: dict, 
                       output: dict, latency: float, success: bool):
        """记录预测日志"""
        log_item = LogItem()
        log_item.set_time(int(time.time()))
        log_item.set_contents([
            ('model_name', model_name),
            ('input', json.dumps(input_data)),
            ('output', json.dumps(output)),
            ('latency_ms', str(latency * 1000)),
            ('success', str(success)),
            ('timestamp', time.strftime('%Y-%m-%d %H:%M:%S'))
        ])
        
        request = PutLogsRequest(self.project, self.logstore, 
                                 topic='model_prediction', 
                                 logitems=[log_item])
        
        self.client.put_logs(request)
    
    def log_model_metrics(self, model_name: str, metrics: dict):
        """记录模型指标"""
        log_item = LogItem()
        log_item.set_time(int(time.time()))
        
        contents = [
            ('model_name', model_name),
            ('metric_type', 'model_performance')
        ]
        
        for key, value in metrics.items():
            contents.append((key, str(value)))
        
        log_item.set_contents(contents)
        
        request = PutLogsRequest(self.project, self.logstore,
                                 topic='model_metrics',
                                 logitems=[log_item])
        
        self.client.put_logs(request)
    
    def create_alert(self, alert_name: str, query: str, 
                     threshold: float, notification: dict):
        """创建告警规则"""
        # 使用 SLS API 创建告警
        # 示例：当模型推理延迟 > 1000ms 时告警
        alert_config = {
            'name': alert_name,
            'query': query,
            'condition': f'latency_ms > {threshold}',
            'notification': notification
        }
        
        return alert_config

# 使用示例
monitor = AIMonitor(
    endpoint='cn-hangzhou.log.aliyuncs.com',
    access_key_id='your-key',
    access_key_secret='your-secret',
    project='ai-project',
    logstore='model-logs'
)

# 记录预测日志
start_time = time.time()
prediction = model.predict(input_data)
latency = time.time() - start_time

monitor.log_prediction(
    model_name='bert-classifier',
    input_data={'text': 'sample input'},
    output={'label': 'positive', 'score': 0.95},
    latency=latency,
    success=True
)

# 记录模型指标
monitor.log_model_metrics(
    model_name='bert-classifier',
    metrics={
        'accuracy': 0.92,
        'precision': 0.90,
        'recall': 0.88,
        'f1_score': 0.89
    }
)
```


## [规则 8] 数据安全与合规 [ENABLED]
# AI 应用数据安全

STATUS: ENABLED
PRIORITY: CRITICAL
说明：
- 使用 KMS 加密敏感数据
- 实施数据脱敏和匿名化
- 遵循 GDPR/PIPL 数据合规要求
- 实施访问控制（RAM）
- 审计数据访问日志

后果：
- 数据泄露导致法律风险和用户信任损失
- 不合规导致监管处罚

示例（数据加密与脱敏）：
```python
from alibabacloud_kms20160120.client import Client as KmsClient
from alibabacloud_kms20160120 import models as kms_models
from alibabacloud_tea_openapi.models import Config
import base64
import re

class DataSecurity:
    def __init__(self, access_key_id: str, access_key_secret: str):
        config = Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret,
            endpoint='kms.cn-hangzhou.aliyuncs.com'
        )
        self.kms_client = KmsClient(config)
    
    def encrypt_data(self, plaintext: str, key_id: str) -> str:
        """使用 KMS 加密数据"""
        request = kms_models.EncryptRequest(
            key_id=key_id,
            plaintext=base64.b64encode(plaintext.encode()).decode()
        )
        
        response = self.kms_client.encrypt(request)
        return response.body.ciphertext_blob
    
    def decrypt_data(self, ciphertext: str) -> str:
        """解密数据"""
        request = kms_models.DecryptRequest(
            ciphertext_blob=ciphertext
        )
        
        response = self.kms_client.decrypt(request)
        plaintext = base64.b64decode(response.body.plaintext).decode()
        return plaintext
    
    @staticmethod
    def mask_phone(phone: str) -> str:
        """手机号脱敏"""
        if len(phone) == 11:
            return phone[:3] + '****' + phone[7:]
        return phone
    
    @staticmethod
    def mask_email(email: str) -> str:
        """邮箱脱敏"""
        if '@' in email:
            local, domain = email.split('@')
            if len(local) > 3:
                masked_local = local[:2] + '***' + local[-1]
            else:
                masked_local = local[0] + '***'
            return f"{masked_local}@{domain}"
        return email
    
    @staticmethod
    def mask_id_card(id_card: str) -> str:
        """身份证脱敏"""
        if len(id_card) == 18:
            return id_card[:6] + '********' + id_card[14:]
        return id_card
    
    def anonymize_user_data(self, user_data: dict) -> dict:
        """用户数据匿名化"""
        anonymized = user_data.copy()
        
        if 'phone' in anonymized:
            anonymized['phone'] = self.mask_phone(anonymized['phone'])
        
        if 'email' in anonymized:
            anonymized['email'] = self.mask_email(anonymized['email'])
        
        if 'id_card' in anonymized:
            anonymized['id_card'] = self.mask_id_card(anonymized['id_card'])
        
        # 移除高敏感字段
        anonymized.pop('password', None)
        anonymized.pop('credit_card', None)
        
        return anonymized

# 使用示例
security = DataSecurity(
    access_key_id='your-key',
    access_key_secret='your-secret'
)

# 加密敏感数据
user_info = "张三,13800138000"
encrypted = security.encrypt_data(
    plaintext=user_info,
    key_id='your-kms-key-id'
)

# 数据脱敏
user_data = {
    'name': '张三',
    'phone': '13800138000',
    'email': 'zhangsan@example.com',
    'id_card': '110101199001011234'
}

anonymized_data = security.anonymize_user_data(user_data)
# 输出: {'name': '张三', 'phone': '138****8000', 
#       'email': 'zh***n@example.com', 'id_card': '110101********1234'}
```


## [规则 9] 成本优化 [ENABLED]
# AI 应用成本管理

STATUS: ENABLED
说明：
- 使用抢占式实例降低训练成本
- 实施模型推理缓存
- 使用 Serverless 按需付费
- 监控和优化 Token 使用
- 实施资源使用配额

示例（成本监控）：
```python
from aliyun.log import LogClient
import json

class CostOptimizer:
    def __init__(self):
        self.token_costs = {
            'qwen-turbo': 0.008,      # 每千 token 价格（元）
            'qwen-plus': 0.02,
            'qwen-max': 0.12
        }
    
    def calculate_llm_cost(self, model: str, 
                           input_tokens: int, 
                           output_tokens: int) -> float:
        """计算大模型调用成本"""
        if model not in self.token_costs:
            raise ValueError(f"未知模型: {model}")
        
        price_per_1k = self.token_costs[model]
        total_tokens = input_tokens + output_tokens
        cost = (total_tokens / 1000) * price_per_1k
        
        return round(cost, 4)
    
    def optimize_prompt(self, prompt: str, max_length: int = 2000) -> str:
        """优化 Prompt 长度"""
        if len(prompt) > max_length:
            # 保留重要信息，截断冗余内容
            return prompt[:max_length] + "..."
        return prompt
    
    def use_cache(self, cache_key: str, cache_store: dict, 
                  compute_fn: callable) -> any:
        """使用缓存减少重复计算"""
        if cache_key in cache_store:
            return cache_store[cache_key], True  # 命中缓存
        
        result = compute_fn()
        cache_store[cache_key] = result
        return result, False
    
    def recommend_instance_type(self, workload: str) -> dict:
        """推荐计算实例类型"""
        recommendations = {
            'training_large': {
                'type': 'ecs.gn6v-c8g1.2xlarge',  # GPU 实例
                'use_spot': True,  # 使用抢占式实例
                'cost_saving': '70%'
            },
            'training_small': {
                'type': 'ecs.c6.xlarge',  # CPU 实例
                'use_spot': False,
                'cost_saving': '0%'
            },
            'inference_realtime': {
                'type': 'pai-eas',  # PAI-EAS 弹性服务
                'autoscaling': True,
                'cost_saving': '40%'
            },
            'inference_batch': {
                'type': 'fc',  # 函数计算 Serverless
                'pay_per_use': True,
                'cost_saving': '60%'
            }
        }
        
        return recommendations.get(workload, {})

# 使用示例
optimizer = CostOptimizer()

# 计算成本
cost = optimizer.calculate_llm_cost(
    model='qwen-turbo',
    input_tokens=500,
    output_tokens=300
)
print(f"调用成本: {cost} 元")

# 使用缓存
cache = {}
result, cached = optimizer.use_cache(
    cache_key='query_123',
    cache_store=cache,
    compute_fn=lambda: expensive_computation()
)

# 获取实例推荐
recommendation = optimizer.recommend_instance_type('training_large')
print(f"推荐实例: {recommendation}")
```


## [规则 10] RAG 架构实现 [ENABLED]
# 检索增强生成

STATUS: ENABLED
PRIORITY: HIGH
说明：
- 使用向量数据库存储知识库
- 实施混合检索（向量 + 关键词 + 重排序）
- 优化 Chunk 切分策略
- 实施上下文窗口管理
- 使用 Rerank 模型提升检索质量

示例（RAG 完整实现）：
```python
from dashvector import Client
from typing import List, Dict
import jieba

class RAGSystem:
    def __init__(self, vector_client, llm_service):
        self.vector_client = vector_client
        self.llm_service = llm_service
        self.chunk_size = 500
        self.chunk_overlap = 50
    
    def chunk_document(self, text: str) -> List[str]:
        """文档分块"""
        chunks = []
        words = list(jieba.cut(text))
        
        for i in range(0, len(words), self.chunk_size - self.chunk_overlap):
            chunk = ''.join(words[i:i + self.chunk_size])
            if len(chunk) > 50:  # 过滤过短的块
                chunks.append(chunk)
        
        return chunks
    
    def hybrid_search(self, query: str, top_k: int = 5) -> List[Dict]:
        """混合检索"""
        # 1. 向量检索
        query_embedding = self.generate_embedding(query)
        vector_results = self.vector_client.search(
            query_vector=query_embedding,
            top_k=top_k * 2
        )
        
        # 2. 关键词检索
        keywords = jieba.lcut_for_search(query)
        keyword_results = self.keyword_search(keywords)
        
        # 3. 结果融合和重排序
        combined_results = self.merge_and_rerank(
            vector_results, 
            keyword_results,
            query
        )
        
        return combined_results[:top_k]
    
    def merge_and_rerank(self, vector_results: List, 
                         keyword_results: List,
                         query: str) -> List[Dict]:
        """结果融合和重排序"""
        # 简化的 RRF (Reciprocal Rank Fusion)
        scores = {}
        
        for rank, result in enumerate(vector_results):
            doc_id = result['id']
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (rank + 60)
        
        for rank, result in enumerate(keyword_results):
            doc_id = result['id']
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (rank + 60)
        
        # 按分数排序
        ranked_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # 构建最终结果
        results = []
        for doc_id, score in ranked_ids:
            # 获取文档内容
            doc = self.get_document(doc_id)
            results.append({
                'id': doc_id,
                'content': doc['content'],
                'score': score
            })
        
        return results
    
    def generate_response(self, query: str, 
                         context_docs: List[Dict]) -> str:
        """生成回答"""
        # 构建上下文
        context = "\n\n".join([
            f"文档 {i+1}:\n{doc['content']}" 
            for i, doc in enumerate(context_docs)
        ])
        
        # 构建 Prompt
        prompt = f"""基于以下参考文档，回答用户问题。如果文档中没有相关信息，请明确说明。

参考文档:
{context}

用户问题: {query}

请提供准确、详细的回答:"""
        
        # 调用 LLM
        messages = [
            {'role': 'system', 'content': '你是一个专业的知识问答助手'},
            {'role': 'user', 'content': prompt}
        ]
        
        response = self.llm_service.chat(messages)
        return response
    
    def query(self, question: str) -> Dict:
        """完整的 RAG 查询流程"""
        # 1. 检索相关文档
        relevant_docs = self.hybrid_search(question, top_k=3)
        
        # 2. 生成回答
        answer = self.generate_response(question, relevant_docs)
        
        # 3. 返回结果
        return {
            'question': question,
            'answer': answer,
            'sources': [
                {'content': doc['content'][:100] + '...', 'score': doc['score']}
                for doc in relevant_docs
            ]
        }

# 使用示例
rag = RAGSystem(
    vector_client=vector_store,
    llm_service=qwen_service
)

# 查询
result = rag.query("什么是向量数据库？")
print(f"回答: {result['answer']}")
print(f"参考来源: {result['sources']}")
```


## [规则 11] Agent 工作流 [DISABLED]
# 构建 AI Agent 应用

STATUS: DISABLED
说明：
- 使用 LangChain/LlamaIndex 框架
- 实施工具调用和链式推理
- 实现 ReAct 模式
- 实施记忆管理
- 使用函数调用能力

示例（Agent 实现）：
```python
from typing import List, Dict, Callable
import json

class Agent:
    def __init__(self, llm_service, tools: List[Dict]):
        self.llm = llm_service
        self.tools = {tool['name']: tool for tool in tools}
        self.memory = []
        self.max_iterations = 5
    
    def think(self, task: str) -> Dict:
        """思考下一步行动"""
        # 构建 Prompt
        prompt = self._build_react_prompt(task)
        
        # 调用 LLM
        functions = [self._tool_to_function(tool) for tool in self.tools.values()]
        response = self.llm.function_calling(
            messages=[{'role': 'user', 'content': prompt}],
            functions=functions
        )
        
        return response
    
    def execute_tool(self, tool_name: str, arguments: Dict) -> any:
        """执行工具"""
        if tool_name not in self.tools:
            raise ValueError(f"未知工具: {tool_name}")
        
        tool = self.tools[tool_name]
        return tool['function'](**arguments)
    
    def run(self, task: str) -> str:
        """运行 Agent"""
        self.memory = [{'role': 'user', 'content': task}]
        
        for i in range(self.max_iterations):
            # 思考
            thought = self.think(task)
            
            if thought['type'] == 'function_call':
                # 执行工具
                tool_name = thought['function']
                arguments = thought['arguments']
                
                observation = self.execute_tool(tool_name, arguments)
                
                # 记录到记忆
                self.memory.append({
                    'action': tool_name,
                    'arguments': arguments,
                    'observation': observation
                })
                
                # 判断是否完成
                if self._is_task_complete(observation):
                    return self._format_final_answer(observation)
            
            elif thought['type'] == 'text':
                # 直接返回答案
                return thought['content']
        
        return "任务未完成，已达到最大迭代次数"
    
    def _build_react_prompt(self, task: str) -> str:
        """构建 ReAct Prompt"""
        prompt = f"""你是一个智能助手，可以使用工具来完成任务。

可用工具:
{self._format_tools()}

任务: {task}

请按照 Thought -> Action -> Observation 的模式思考和行动。
"""
        return prompt
    
    def _format_tools(self) -> str:
        """格式化工具描述"""
        tools_desc = []
        for name, tool in self.tools.items():
            tools_desc.append(f"- {name}: {tool['description']}")
        return "\n".join(tools_desc)

# 定义工具
def search_knowledge_base(query: str) -> str:
    """搜索知识库"""
    # 实际实现
    return f"搜索结果: {query}"

def calculate(expression: str) -> float:
    """计算数学表达式"""
    return eval(expression)

tools = [
    {
        'name': 'search_knowledge_base',
        'description': '在知识库中搜索相关信息',
        'function': search_knowledge_base,
        'parameters': {'query': 'string'}
    },
    {
        'name': 'calculate',
        'description': '计算数学表达式',
        'function': calculate,
        'parameters': {'expression': 'string'}
    }
]

# 使用 Agent
agent = Agent(llm_service=qwen_service, tools=tools)
result = agent.run("帮我查找关于向量数据库的信息，并计算 100 * 0.8")
```


## [规则 12] 持续优化与迭代 [ENABLED]
# AI 应用持续改进

STATUS: ENABLED
说明：
- 收集用户反馈和评分
- 实施 A/B 测试
- 监控模型性能退化
- 定期重训练和更新模型
- 实施人工审核机制

示例（反馈收集与优化）：
```python
import time
from typing import Optional

class FeedbackSystem:
    def __init__(self, log_client):
        self.log_client = log_client
        self.feedback_store = {}
    
    def collect_feedback(self, query_id: str, 
                         rating: int, 
                         feedback_text: Optional[str] = None):
        """收集用户反馈"""
        feedback = {
            'query_id': query_id,
            'rating': rating,  # 1-5 星
            'feedback_text': feedback_text,
            'timestamp': time.time()
        }
        
        self.feedback_store[query_id] = feedback
        
        # 记录到日志
        self.log_client.log_prediction(
            model_name='feedback',
            input_data={'query_id': query_id},
            output={'rating': rating},
            latency=0,
            success=True
        )
    
    def analyze_feedback(self, time_range: str = '7d') -> Dict:
        """分析反馈数据"""
        # 从日志服务查询反馈数据
        # 计算平均评分、低分比例等
        
        total_feedback = len(self.feedback_store)
        if total_feedback == 0:
            return {'avg_rating': 0, 'low_rating_ratio': 0}
        
        ratings = [f['rating'] for f in self.feedback_store.values()]
        avg_rating = sum(ratings) / len(ratings)
        low_rating_count = sum(1 for r in ratings if r <= 2)
        low_rating_ratio = low_rating_count / total_feedback
        
        return {
            'total_feedback': total_feedback,
            'avg_rating': round(avg_rating, 2),
            'low_rating_ratio': round(low_rating_ratio, 2),
            'needs_improvement': low_rating_ratio > 0.2
        }
    
    def ab_test(self, user_id: str, variants: List[str]) -> str:
        """A/B 测试分流"""
        # 基于用户 ID 哈希分流
        hash_value = hash(user_id) % len(variants)
        return variants[hash_value]

# 使用示例
feedback_sys = FeedbackSystem(log_client=monitor)

# 收集反馈
feedback_sys.collect_feedback(
    query_id='query_123',
    rating=4,
    feedback_text='回答很准确'
)

# 分析反馈
analysis = feedback_sys.analyze_feedback(time_range='7d')
if analysis['needs_improvement']:
    print("检测到用户满意度下降，需要优化模型")

# A/B 测试
variant = feedback_sys.ab_test(
    user_id='user_456',
    variants=['model_v1', 'model_v2']
)
```


# ============================================
# 项目类型配置
# ============================================

智能客服系统：
- 启用： [规则 1, 2, 3, 6, 7, 8, 10, 12]
- 关键：模型服务化、向量检索、大模型调用、RAG、监控

推荐系统：
- 启用： [规则 1, 4, 5, 6, 7, 9]
- 关键：特征工程、模型训练、实时推理、成本优化

智能搜索：
- 启用： [规则 2, 3, 7, 10, 12]
- 关键：向量检索、大模型、RAG、持续优化

AI Agent 应用：
- 启用： [规则 1, 3, 7, 8, 10, 11, 12]
- 关键：模型服务、大模型、RAG、Agent 工作流


# ============================================
# 与其他规范的集成
# ============================================

DEPENDENCIES:
  alibaba-cloud-ai-spec.txt::RULE 6 -> deployment-spec.txt::RULE 3
    note: 推理服务部署遵循容器化部署规范
  alibaba-cloud-ai-spec.txt::RULE 7 -> error-handling-spec.txt::RULE 3
    note: 监控日志遵循日志记录规范
  alibaba-cloud-ai-spec.txt::RULE 8 -> security-spec.txt::RULE 3
    note: 数据安全遵循安全规范


# ============================================
# 摘要 - 启用的规则
# ============================================

✅ [规则 1]  模型服务化架构 - PAI 模型部署
✅ [规则 2]  向量检索存储 - DashVector/Hologres
✅ [规则 3]  大模型调用管理 - 通义千问集成
✅ [规则 4]  数据湖特征工程 - OSS/MaxCompute/Feature Store
✅ [规则 5]  模型训练优化 - PAI-DLC 分布式训练
✅ [规则 6]  实时推理服务 - PAI-EAS 弹性推理
✅ [规则 7]  监控可观测性 - SLS/ARMS 全链路监控
✅ [规则 8]  数据安全合规 - KMS 加密/数据脱敏
✅ [规则 9]  成本优化 - 抢占式实例/缓存/Serverless
✅ [规则 10] RAG 架构实现 - 检索增强生成
✅ [规则 12] 持续优化迭代 - 反馈收集/A/B 测试


# ============================================
# 阿里云产品映射
# ============================================

AI 平台：
- PAI（Platform for AI）- 模型训练和部署
- 通义千问（DashScope）- 大语言模型
- DashVector - 向量检索服务

数据存储：
- OSS - 对象存储/数据湖
- MaxCompute - 大数据计算
- Hologres - 实时数仓/向量数据库
- AnalyticDB - 云原生数据仓库

监控运维：
- SLS（日志服务）- 日志采集分析
- ARMS - 应用实时监控
- CloudMonitor - 云监控

安全合规：
- KMS - 密钥管理服务
- RAM - 访问控制
- ActionTrail - 操作审计


# ============================================
# 版本历史
# ============================================
# v1.0 (2025-11-10) - 初始阿里云 AI 卓越架构规范，包含 12 条规则
# ============================================
