import torch
from transformers import BertForSequenceClassification, BertTokenizer


class TextAnalyzer:
    def __init__(self):
        # 加载BERT tokenizer和模型
        self.tokenizer = BertTokenizer.from_pretrained('model/bert-base-chinese')
        self.model = BertForSequenceClassification.from_pretrained('model/bert-base-chinese')
        # 加载微调后的模型参数
        checkpoint = torch.load('model/fine_bert_model.pth')
        num_labels = 6  # 你的任务标签数量
        # 创建新的输出层参数
        old_out_weight = checkpoint["classifier.weight"]
        old_out_bias = checkpoint["classifier.bias"]
        new_out_weight = torch.zeros((num_labels, old_out_weight.shape[1]))
        new_out_bias = torch.zeros((num_labels,))
        new_out_weight[:old_out_weight.shape[0], :] = old_out_weight
        new_out_bias[:old_out_bias.shape[0]] = old_out_bias

        # 更新模型的输出层参数
        self.model.classifier.weight.data = new_out_weight
        self.model.classifier.bias.data = new_out_bias
        # 加载微调后的模型参数
        self.model.load_state_dict(checkpoint)

        # 将模型设置为评估模式
        self.model.eval()

    def analyze_text(self, text):
        # 使用模型进行推理
        inputs = self.tokenizer(text, return_tensors="pt")
        outputs = self.model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()

        # 打印结果
        emotion_mapping = {0: 'neutral', 1: 'happy', 2: 'angry', 3: 'sad', 4: 'fear', 5: 'surprise'}
        predicted_emotion = emotion_mapping[predicted_class]
        return predicted_emotion