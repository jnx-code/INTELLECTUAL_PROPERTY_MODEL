import sys
from main import CopyrightDetectionSystem
from dataset_generator import create_dataset

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def evaluate():
    print("Initializing Model and Database...")
    system = CopyrightDetectionSystem()
    system.initialize(force_rebuild=True)  # Forces fresh training
    
    print("\nExtracting Evaluation Benchmark Queries...")
    _, test_queries = create_dataset()
    
    # Run Accuracy loop
    total_queries = len(test_queries)
    top_1_correct = 0
    top_3_correct = 0
    valid_queries = 0
    
    print("\n" + "=" * 80)
    print("MODEL ACCURACY EVALUATION")
    print("=" * 80)
    for tq in test_queries:
        if tq["expected_match"] is None:
            # Skip "No-Match" tests since it's testing true negative threshold, not retrieval
            continue
            
        valid_queries += 1
        query_text = tq["query"]
        expected = tq["expected_match"]
        term_type = tq["similarity_type"]
        
        report = system.analyze(query_text, top_k=3)
        matches = report.attributions
        
        print(f"\nQuery ({term_type}): {query_text[:50]}...")
        print(f"Target: {expected}")
        
        rank = -1
        for i, match in enumerate(matches):
            if match["title"] == expected:
                rank = i
                break
                
        if rank == 0:
            print("[Pass] Top-1 Match ✓")
            top_1_correct += 1
            top_3_correct += 1
        elif rank >= 0 and rank < 3:
            print(f"[Pass] Top-3 Match (Rank {rank+1}) ✓")
            top_3_correct += 1
        else:
            print("[Fail] Model failed to retrieve the target in Top 3 ❌")
            if matches:
                print(f"       Closest found was: {matches[0]['title']}")
                
    # Final Metrics
    print("\n" + "=" * 80)
    print("FINAL ACCURACY SCORES")
    print("=" * 80)
    
    p1 = top_1_correct / valid_queries * 100 if valid_queries > 0 else 0
    p3 = top_3_correct / valid_queries * 100 if valid_queries > 0 else 0
    
    print(f"Precision@1 (Top-1 Accuracy): {p1:.2f}%")
    print(f"Precision@3 (Top-3 Accuracy): {p3:.2f}%")
    print(f"Total Valid Benchmark Tasks:  {valid_queries}")

if __name__ == "__main__":
    evaluate()
