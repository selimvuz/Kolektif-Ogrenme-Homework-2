import tensorflow as tf
import numpy as np
import json
import pandas as pd
from transformers import BertTokenizer, TFBertForSequenceClassification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Toplam model sayısı
num_models = 5

# Önceden eğitilmiş BERT modelini ve tokenizer'ı yükleyin
tokenizer = BertTokenizer.from_pretrained("Models/model_1")

# Fine-tune edilmiş modelleri yükleyin
models = []
for i in range(1, num_models + 1):
    model = TFBertForSequenceClassification.from_pretrained(
        f"Models/model_{i}")
    models.append(model)

# Bir örnek metin ve etiket oluşturun
max_length = 128
# Gerçek örneğinizi girin
sample_text = "hiç beğenmedim çok kötüydü 1 yıldız bile fazla"
sample_encodings = tokenizer([sample_text], truncation=True,
                             padding=True, max_length=max_length, return_tensors="tf")
sample_label = 1


def convert_to_tensors(hashable_encodings):
    return {k: np.array(v) for k, v in hashable_encodings.items()}


def convert_to_hashable(batch_encoding):
    return {k: tuple(v.numpy()) for k, v in batch_encoding.items()}


hashable_encodings = convert_to_hashable(sample_encodings)
tensor_encodings = convert_to_tensors(hashable_encodings)

# Her modelin tahminlerini ve gerçek değerleri yazdırın
for i, model in enumerate(models):
    model_prediction = model.predict(tensor_encodings)
    model_prediction_label = np.argmax(model_prediction["logits"])

    print(
        f"Model {i + 1} - Tahmini Değer: {model_prediction_label}, Gerçek Değer: {sample_label}")

# Averaging yöntemiyle ensemble tahmini yapın
ensemble_predictions = np.zeros((1, num_models))

for i, model in enumerate(models):
    model_prediction = model.predict(tensor_encodings)
    ensemble_predictions[0, i] = tf.argmax(model_prediction["logits"], axis=1)

# Sonucu hesapla
ensemble_prediction_avg = int(np.round(np.mean(ensemble_predictions)))

# Tahmini yazdır
print(
    f"\nEnsemble Tahmini (Averaging): {ensemble_prediction_avg}, Gerçek Değer: {sample_label}")
