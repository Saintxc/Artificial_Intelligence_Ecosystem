## Description of the document you selected

I chose the wikipedia article about Grizzly Bear's, had to match the previous project.


---

## 5 important questions and answers

### 1. Why do we need embeddings in a RAG system, and how does the embedding dimensionality matter?

**Answer:**
Embeddings convert text into dense vectors that capture semantic meaning. In your system, sentence-transformers/all-distilroberta-v1 produces 768-dimensional vectors. Dimensionality matters because it determines how much nuance can be encoded. Too few dimensions may miss subtle meaning, while too many can increase memory/computation costs without major gains. FAISS relies on consistent embedding dimensionality to compare query and document vectors.

---

### 2. How does FAISS actually find relevant chunks, and what does L2 distance mean here?

**Answer:**
FAISS (Facebook AI Similarity Search) indexes all chunk embeddings and compares a query embedding against them. With IndexFlatL2, it computes Euclidean (L2) distance between vectors. Smaller distances mean higher similarity. It returns the indices of the closest chunks, which you then map back to the original text segments. Using L2 is straightforward and works well for sentence embeddings, though cosine similarity is another common option.
---

### 3. Why do we use chunking with overlap, and how do chunk size and overlap affect retrieval quality?

**Answer:**
Chunking ensures that the model can process long documents by splitting them into smaller, semantically meaningful units. Your system uses a chunk_size=500 and chunk_overlap=50. The overlap prevents important context from being cut off at chunk boundaries — without overlap, sentences split across chunks could lose meaning. Too small chunks risk losing context, while too large chunks may exceed model context limits or dilute retrieval accuracy.

---

### 4. How does prompt design influence the quality of answers in a RAG pipeline?

**Answer:**
Prompt design controls how well the language model uses retrieved context. In your case, the prompt explicitly tells the model: “If the answer is not in the context, say you don’t know.” This reduces hallucination and forces answers to be grounded in retrieved text. Clear separation of Context, Question, and Answer also helps the model parse instructions correctly. Weak prompt design could lead to fabricated or ungrounded answers.

---

### 5. What are potential limitations of this RAG system, and how could it be improved?

**Answer:**
Current limitations include:

1. Embedding model quality: The chosen model may not capture deep semantics as well as larger models.

2. Exact search: Using only L2 search may miss nuances; approximate nearest neighbor search could improve scalability.

3. Context stitching: The retrieved chunks are concatenated without filtering redundancy.

4. Generation model: If using a small local model (like FLAN-T5), the answers may be short or vague. Improvements could include using larger embedding models, hybrid search (keyword + vector), re-ranking retrieved chunks, and upgrading the LLM for more robust answer generation.

---

## 3 Questions and Answer Quality

**Your question:** How much does a grizzly bear weigh?
**Answer:** The weight of a grizzly bear can vary depending on the population and location. For example, males in the coastal grizzlies in the Alaskan peninsula can weigh around 389 kilograms (858 lb), while females can weigh around 207 kilograms (456 lb).


**Your question:** How long are a grizzly bears claws?
**Answer:** I don't know.


**Your question:** Where can you find grizzly bears?
**Answer:** You can find grizzly bears in Alaska, western Canada, and portions of the northwestern United States such as Washington, Idaho, Montana, and Wyoming. They can also be found in specific areas like Yellowstone and Grand Teton National Parks, the Northern Continental Divide in Montana, the Greater Yellowstone Ecosystem in Wyoming, Idaho, and Montana, and the Selway-Bitterroot Wilderness ecosystem in Idaho.

The quality of the answers were decently informative, but things like claw size should be within the article.

To test what happens when I change the chunk size and overlap size, I asked the RAG model "How big area grizzly bears claws?", which is something I know the Wikipedia article had a section on. Seems even with the increased chunk/ overlap changes it still can't answer anything about the claws. Instead I asked it "what do you know about grizzly bear claws?"

**Chunk size = 1000**
**Overlap = 500**

**Answer:** Grizzly bears have sharp claws that they use for various purposes, including digging, climbing, and defending themselves. They can also use their claws to harass other predators during interactions over food sources or kills.

**Chunk size = 500**
**Chunk overlap = 100**

**Answer:** Based on the provided context, cougars use their claws to harass grizzly bears when in disputes over kills. They rely on their superior agility and claws to stay out of the bear's reach until one of them gives up. Grizzly bears, on the other hand, may retaliate against wolves by sitting down and using their ability to protect themselves in a full circle when the wolves become aggressive with quick nips at their hind legs.


**Chunk size = 100**
**Chunk overlap = 50**

**Answer:** The claws of bears and cougars are used for chasing and pinning fish, as well as for harassing other animals.


In general, it seems like the shorter the chunk size and the less the chunk overlap, the less detailed the answer is.