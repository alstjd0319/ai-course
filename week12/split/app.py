import base64, json, re
from openai import OpenAI
from flask import Flask, render_template, request, jsonify

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

app = Flask(__name__)

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process_receipt', methods=['POST'])
def process_receipt():
    try:
        if 'receipt_image' not in request.files:
            return jsonify({"error": "이미지가 없습니다."}), 400
        
        file = request.files['receipt_image']
        people_count = int(request.form.get('people', 1))
        
        if people_count <= 0:
            return jsonify({"error": "인원수는 1명 이상이어야 합니다."}), 400

        image_bytes = file.read()
        
        prompt = "영수증 이미지에서 항목명과 금액을 추출해서 JSON 형식으로만 응답해줘. 형식은 [{\"item\": \"항목명\", \"amount\": 1000}, ...] 형태여야 해. 다른 설명은 하지 마."
        
        ai_response = ask(prompt, image_bytes=image_bytes)
        items = parse_json(ai_response)

        if items is None:
            return jsonify({"error": "읽지 못했습니다."}), 400

        total_amount = sum(item['amount'] for item in items)
        per_person = total_amount // people_count

        return jsonify({
            "items": items,
            "total_amount": total_amount,
            "per_person": per_person
        })

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "처리 중 오류가 발생했습니다."}), 500

if __name__ == '__main__':
    app.run(debug=True)
