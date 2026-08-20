from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"

history = []

assessment = [
    ["LLM01", "Prompt Injection", "Yes", "High",
     "Use strong instruction hierarchy and input filtering."],

    ["LLM02", "Insecure Output Handling", "Yes", "High",
     "Sanitize and encode model-generated output before rendering."],

    ["LLM03", "Training Data Poisoning", "No", "Low",
     "Validate training and fine-tuning data sources."],

    ["LLM04", "Model Denial of Service", "Yes", "Medium",
     "Use token limits, rate limiting and resource controls."],

    ["LLM05", "Supply Chain Vulnerabilities", "Yes", "Medium",
     "Verify dependencies and use trusted, pinned versions."],

    ["LLM06", "Sensitive Information Disclosure", "No", "Low",
     "Protect secrets and prevent disclosure of internal information."],

    ["LLM07", "Insecure Plugin Design", "No", "Low",
     "Use authorization and explicit user confirmation."],

    ["LLM08", "Excessive Agency", "No", "Low",
     "Require authorization before performing external actions."],

    ["LLM09", "Overreliance", "No", "Low",
     "Communicate uncertainty and require verification of important information."],

    ["LLM10", "Model Theft", "No", "Low",
     "Protect model configuration and restrict unauthorized access."]
]


HTML = """
<!DOCTYPE html>
<html>

<head>

<title>AI Security Lab</title>

<style>

body {
    font-family: Arial, sans-serif;
    max-width: 1100px;
    margin: 30px auto;
    padding: 20px;
}

h1 {
    text-align: center;
}

h2 {
    margin-top: 40px;
}

textarea {
    width: 100%;
    height: 120px;
    padding: 10px;
    font-size: 16px;
    box-sizing: border-box;
}

button {
    margin-top: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

.response {
    margin-top: 25px;
    padding: 20px;
    background: #f2f2f2;
    border-radius: 8px;
    white-space: pre-wrap;
}

.prompt {
    font-weight: bold;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
    font-size: 14px;
}

th, td {
    border: 1px solid #999;
    padding: 10px;
    text-align: left;
    vertical-align: top;
}

th {
    background: #e6e6e6;
}

</style>

</head>

<body>

<h1>AI Security Lab</h1>

<form method="POST" action="/chat">

<label>
<b>Enter your message:</b>
</label>

<br><br>

<textarea
name="message"
placeholder="Ask the AI something..."
></textarea>

<br>

<button type="submit">Send</button>

</form>


{% for item in history %}

<div class="response">

<div class="prompt">
Prompt:
</div>

{{ item.prompt }}

<hr>

<b>AI Response:</b>

<br><br>

{{ item.response }}

</div>

{% endfor %}


<h2>OWASP LLM Top 10 Assessment</h2>

<table>

<tr>
<th>Category</th>
<th>Test Performed</th>
<th>Triggered?</th>
<th>Severity</th>
<th>Remediation</th>
</tr>

{% for row in assessment %}

<tr>

<td>{{ row[0] }}</td>

<td>{{ row[1] }}</td>

<td>{{ row[2] }}</td>

<td>{{ row[3] }}</td>

<td>{{ row[4] }}</td>

</tr>

{% endfor %}

</table>

</body>

</html>
"""


@app.route("/", methods=["GET"])
def home():

    return render_template_string(
        HTML,
        history=history,
        assessment=assessment
    )


@app.route("/chat", methods=["POST"])
def chat():

    message = request.form.get("message", "")

    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": message,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get(
            "response",
            "No response returned."
        )

    except requests.exceptions.RequestException as e:

        answer = f"Error communicating with Ollama: {e}"

    history.append({
        "prompt": message,
        "response": answer
    })

    return render_template_string(
        HTML,
        history=history,
        assessment=assessment
    )


if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )
