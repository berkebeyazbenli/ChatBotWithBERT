
from transformers import TFDistilBertForQuestionAnswering, DistilBertTokenizer
import tensorflow as tf
import random

class Chatbot:
    def __init__(self):
        try:
            self.model_name = 'distilbert-base-cased'
            self.model = TFDistilBertForQuestionAnswering.from_pretrained(self.model_name)
            self.tokenizer = DistilBertTokenizer.from_pretrained(self.model_name)
            
            
            self.responses = {
                "merhaba": "merhaba nasıl yardımcı olabilirim?",
                "hava": "Bugün hava oldukça güzel",
                "yemek": "En sevdiğim yemek makarna",
                "kitap": "istersen kitap önerisi verebilirim",
                "teşekkür": " Başka bir şey sormak isterseniz buradayım.",
                "fenerbahçe": "Türkiyenin en büyük spor kulübünden mi bahsediyorsun",
                "euro2024": "Belki Türkiye şampiyon olur ne diyorsun",
                "selam": "selam nasıl yardımcı olabilirim"
            }
        except Exception as e:
            print("Error")

    def get_response(self, user_input):
        if not user_input.strip():
            return "yazın."

        for keyword, response in self.responses.items():
            if keyword in user_input.lower():
                return response

        return "anlamadım"

    def process_input(self, user_input):
        ### Metni tokenizer kullanarak tensörlere dönüştürür...Matris ya da dizi gibi düşünebiliriz
        inputs = self.tokenizer(user_input, return_tensors="tf")
        input_ids = inputs["input_ids"]  # Girişler için token ID'leri
        attention_mask = inputs["attention_mask"] ##Dikkat etmesi gereken yerler

        return input_ids, attention_mask

    def answer_question(self, user_input):
        ##user inputu alarak modele anlyacağı şekle dönüştürür
        input_ids, attention_mask = self.process_input(user_input)
        output = self.model(input_ids=input_ids, attention_mask=attention_mask)
        ### Başlangıç ve bitiş skorlarını alır..Potansiyel cevaplar içim başlangıç ve bitiş belirlemek için
        start_scores = output.start_logits
        end_scores = output.end_logits

        ##Tokenları dönüştürürr.
        all_tokens = self.tokenizer.convert_ids_to_tokens(input_ids.numpy().squeeze())
        
        ##başlangıç ve sona göre uygun tokenları seçmek için
        answer_tokens = all_tokens[tf.argmax(start_scores, axis=1)[0] : tf.argmax(end_scores, axis=1)[0] + 1]
        
        ##aldığı tokenları string ifadeye dönüşterek uygun sonucu veriyor(en yüksek tokenları seçiyor)
        chatbot_response = self.tokenizer.convert_tokens_to_string(answer_tokens)

        return chatbot_response