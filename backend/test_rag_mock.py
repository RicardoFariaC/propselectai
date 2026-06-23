import sys, os
sys.path.append('/home/ricardo/Documents/Mestrado/Aulas/IA_2026_1/EXAME/backend')

from models.schemas import PropellerRequest
import services.rag

# Mock api key
services.rag.OPENAI_API_KEY = "dummy"

# Mock Chroma
class DummyDoc:
    def __init__(self, c, s, p, d):
        self.page_content = c
        self.metadata = {'source': s, 'page': p, 'doc_id': d}

class DummyVectorStore:
    def similarity_search(self, q, k):
        return [DummyDoc("Content", "doc1.pdf", 1, "doc1")]

class DummyChroma:
    def __init__(self, *args, **kwargs):
        pass
    def similarity_search(self, q, k=5):
        return [DummyDoc("Content", "doc1.pdf", 1, "doc1")]

services.rag.Chroma = DummyChroma

# Mock LLM
class DummyLLM:
    def __init__(self, *args, **kwargs):
        pass
    def invoke(self, *args, **kwargs):
        class Resp:
            content = "This is a justification [1]"
        return Resp()
services.rag.ChatOpenAI = DummyLLM

class DummyChain:
    def invoke(self, args):
        class Resp:
            content = "This is a justification [1]"
        return Resp()

services.rag.PromptTemplate.__or__ = lambda self, other: DummyChain()

prop = {
    'nome_helice': 'APC 10x5E',
    'diametro': 10,
    'pitch': 5,
    'eficiência': 0.75,
    'trust_n': 15.0
}
req = PropellerRequest(
    mission_type='reconhecimento',
    weight_kg=2.5,
    engine_power_hp=1.0,
    cruise_speed_ms=10.0
)

try:
    text, refs = services.rag.generate_justification(prop, req)
    print("TEXT:")
    print(text)
    print("REFS:")
    print(refs)
except Exception as e:
    import traceback
    traceback.print_exc()
