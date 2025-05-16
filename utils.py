"""
Utility functions for the prize drawing application.
"""
import pandas as pd
import io
import random
import json

def calculate_probabilities(participants):
    """
    Calculate the drawing probability for each participant.
    
    Args:
        participants: List of dictionaries with name and tickets
        
    Returns:
        List of dictionaries with name, tickets, and probability
    """
    if not participants:
        return []
    
    total_tickets = sum(p["tickets"] for p in participants)
    if total_tickets == 0:
        return [{"name": p["name"], "tickets": p["tickets"], "probability": 0} for p in participants]
    
    result = []
    for p in participants:
        probability = (p["tickets"] / total_tickets) * 100
        result.append({
            "name": p["name"],
            "tickets": p["tickets"],
            "probability": round(probability, 2)
        })
    
    return result

def select_winner(participants):
    """
    Select a winner based on ticket distribution.
    
    Args:
        participants: List of dictionaries with name and tickets
        
    Returns:
        Dictionary with the winner's name and tickets
    """
    if not participants:
        return None
    
    # Create a pool of tickets where each participant appears according to their ticket count
    ticket_pool = []
    for p in participants:
        ticket_pool.extend([p["name"]] * p["tickets"])
    
    if not ticket_pool:
        # If no tickets, select randomly from the participants
        return random.choice(participants)
    
    # Select a random ticket
    winning_name = random.choice(ticket_pool)
    
    # Find the participant with the winning name
    for p in participants:
        if p["name"] == winning_name:
            return p
    
    return None

def save_to_csv(participants):
    """
    Convert participants to CSV format for download.
    
    Args:
        participants: List of dictionaries with name and tickets
        
    Returns:
        CSV string
    """
    if not participants:
        return "name,tickets\n"
    
    df = pd.DataFrame(participants)
    output = io.StringIO()
    df.to_csv(output, index=False)
    return output.getvalue()

def load_from_csv(csv_content):
    """
    Load participants from CSV content.
    
    Args:
        csv_content: CSV string
        
    Returns:
        List of dictionaries with name and tickets
    """
    try:
        df = pd.read_csv(io.StringIO(csv_content))
        if 'name' not in df.columns or 'tickets' not in df.columns:
            return None
        
        participants = []
        for _, row in df.iterrows():
            participants.append({
                "name": row['name'],
                "tickets": int(row['tickets'])
            })
        return participants
    except Exception:
        return None
