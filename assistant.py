class HackerAI_Logic:
    async def generate_response(self, query):
        query = query.lower()
        
        if "payload" in query or "exploit" in query:
            return ("⚠️ **Pentest Guidance:** When generating payloads for authorized testing, "
                    "ensure you are using updated meterpreter templates for the target architecture. "
                    "Which OS are you targeting (Android/Windows/Linux)?")
            
        if "python" in query or "code" in query:
            return "🖥️ **Code Assistant:** I can help you write Python scrapers, automation scripts, or socket listeners. Describe your logic."

        return "I am ready for the task. Provide the technical parameters for the security assessment."
