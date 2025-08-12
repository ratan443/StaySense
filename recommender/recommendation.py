from typing import List, Dict

"""
    Rank items based on semantic similarity + user preferences.
    
    Args:
        retrieved_items: List of items from RAG retrieval (with metadata).
        user_prefs: Dictionary of user preferences (e.g., {'budget': 200, 'location': 'beach', 'amenities': ['wifi']}).
        
    Returns:
        Ranked list of items.
    """
def recommendation_scorer(retrieved_items: List[Dict], user_prefs: Dict):
    ranked = []
    for item in retrieved_items:
        score = 0

        if "price" in item and item["price"] <= user_prefs.get("budget", float("inf")):
            score += 2

        if "location" in item and user_prefs.get("location", "").lower() in item["location"].lower():
            score += 3

        if "amenities" in item:
            all_amenities = set(item["amenities"]).intersection(set(user_prefs.get("amenities", [])))
            score += len(all_amenities)
        
        item["score"] = score
        ranked.append(item)
    
    # Sort by highest scores first, as we want these picked off the top
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked

if __name__ == "__main__":
    # do something here later