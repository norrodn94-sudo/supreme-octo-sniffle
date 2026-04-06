import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional

class HVACLead:
    """Represents a single HVAC lead."""
    
    def __init__(self, name: str, email: str, phone: str, address: str, 
                 service_type: str, budget: Optional[float] = None):
        self.id = str(uuid.uuid4())
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.service_type = service_type  # maintenance, repair, installation, inspection
        self.budget = budget
        self.created_at = datetime.now().isoformat()
        self.status = "new"  # new, contacted, qualified, converted, lost
        self.notes = ""
    
    def to_dict(self) -> Dict:
        """Convert lead to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'service_type': self.service_type,
            'budget': self.budget,
            'created_at': self.created_at,
            'status': self.status,
            'notes': self.notes
        }


class HVACLeadGenerator:
    """Manages HVAC lead generation and tracking."""
    
    def __init__(self):
        self.leads: List[HVACLead] = []
    
    def add_lead(self, name: str, email: str, phone: str, address: str,
                 service_type: str, budget: Optional[float] = None) -> HVACLead:
        """Add a new HVAC lead."""
        lead = HVACLead(name, email, phone, address, service_type, budget)
        self.leads.append(lead)
        return lead
    
    def get_lead(self, lead_id: str) -> Optional[HVACLead]:
        """Retrieve a lead by ID."""
        for lead in self.leads:
            if lead.id == lead_id:
                return lead
        return None
    
    def update_lead_status(self, lead_id: str, status: str) -> bool:
        """Update lead status."""
        lead = self.get_lead(lead_id)
        if lead:
            lead.status = status
            return True
        return False
    
    def add_lead_notes(self, lead_id: str, notes: str) -> bool:
        """Add notes to a lead."""
        lead = self.get_lead(lead_id)
        if lead:
            lead.notes += f"\n[\{datetime.now().isoformat()}] {notes}"
            return True
        return False
    
    def get_leads_by_status(self, status: str) -> List[HVACLead]:
        """Get all leads with a specific status."""
        return [lead for lead in self.leads if lead.status == status]
    
    def get_leads_by_service_type(self, service_type: str) -> List[HVACLead]:
        """Get all leads requesting a specific service."""
        return [lead for lead in self.leads if lead.service_type == service_type]
    
    def get_high_value_leads(self, min_budget: float) -> List[HVACLead]:
        """Get leads with budget >= min_budget."""
        return [lead for lead in self.leads if lead.budget and lead.budget >= min_budget]
    
    def export_leads(self, filename: str = 'hvac_leads.json') -> None:
        """Export all leads to JSON file."""
        leads_data = [lead.to_dict() for lead in self.leads]
        with open(filename, 'w') as f:
            json.dump(leads_data, f, indent=2)
    
    def get_statistics(self) -> Dict:
        """Get lead statistics."""
        total_leads = len(self.leads)
        status_breakdown = {}
        service_breakdown = {}
        total_budget = 0
        leads_with_budget = 0
        
        for lead in self.leads:
            status_breakdown[lead.status] = status_breakdown.get(lead.status, 0) + 1
            service_breakdown[lead.service_type] = service_breakdown.get(lead.service_type, 0) + 1
            if lead.budget:
                total_budget += lead.budget
                leads_with_budget += 1
        
        return {
            'total_leads': total_leads,
            'status_breakdown': status_breakdown,
            'service_breakdown': service_breakdown,
            'average_budget': total_budget / leads_with_budget if leads_with_budget > 0 else 0,
            'total_potential_revenue': total_budget
        }


if __name__ == '__main__':
    # Example usage
    generator = HVACLeadGenerator()
    
    # Add sample leads
    lead1 = generator.add_lead(
        name='John Smith',
        email='john@example.com',
        phone='555-0123',
        address='123 Main St, Springfield, IL',
        service_type='maintenance',
        budget=500
    )
    
    lead2 = generator.add_lead(
        name='Jane Doe',
        email='jane@example.com',
        phone='555-0456',
        address='456 Oak Ave, Springfield, IL',
        service_type='installation',
        budget=5000
    )
    
    # Update statuses
    generator.update_lead_status(lead1.id, 'contacted')
    generator.add_lead_notes(lead1.id, 'Customer interested in spring maintenance package')
    
    # Print statistics
    print('HVAC Lead Generator Statistics:')
    print(json.dumps(generator.get_statistics(), indent=2))
    
    # Export leads
    generator.export_leads()
    print('\nLeads exported to hvac_leads.json')