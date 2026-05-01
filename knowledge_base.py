# Simple Knowledge Base with Resolution Refutation
# This module handles Propositional Logic and proof by contradiction

class Clause:
    """Represents a clause in CNF (disjunction of literals)"""
    def __init__(self, literals=None):
        if literals is None:
            self.literals = set()
        else:
            self.literals = set(literals)
    
    def __repr__(self):
        return str(sorted(self.literals))
    
    def __eq__(self, other):
        return self.literals == other.literals
    
    def __hash__(self):
        return hash(frozenset(self.literals))


class KnowledgeBase:
    """Simple Knowledge Base for Wumpus World using Propositional Logic"""
    
    def __init__(self):
        self.clauses = set()
        self.inference_steps = 0
    
    def add_rule(self, rule_text):
        """
        Add rules in simple format: 
        - "safe_2_1" adds safe cell
        - "breeze_1_1 OR pit_2_1 OR pit_1_2 OR pit_1_0" adds OR clause
        - "NOT pit_2_1" adds negation
        """
        self.clauses.add(Clause([rule_text]))
    
    def add_clause(self, literals):
        """Add a clause (list of literals)"""
        clause = Clause(literals)
        self.clauses.add(clause)
    
    def negate(self, literal):
        """Return negation of a literal"""
        if literal.startswith("NOT "):
            return literal[4:]
        else:
            return "NOT " + literal
    
    def resolve(self, clause1, clause2, literal):
        """
        Resolve two clauses on a literal
        Returns the resolvent or None if resolution fails
        """
        # Create resolvent by removing the literal and its negation
        resolvent_literals = (clause1.literals - {literal}) | (clause2.literals - {self.negate(literal)})
        
        if len(resolvent_literals) == 0:
            # Empty clause - contradiction found!
            return Clause([])
        
        return Clause(resolvent_literals)
    
    def find_resolvable_clauses(self, literal):
        """Find pairs of clauses that can be resolved on a literal"""
        resolvable = []
        neg_literal = self.negate(literal)
        
        clause_list = list(self.clauses)
        for i, c1 in enumerate(clause_list):
            for c2 in clause_list[i+1:]:
                if literal in c1.literals and neg_literal in c2.literals:
                    resolvable.append((c1, c2, literal))
                elif neg_literal in c1.literals and literal in c2.literals:
                    resolvable.append((c1, c2, self.negate(literal)))
        
        return resolvable
    
    def prove(self, query):
        """
        Prove a query using Resolution Refutation
        Returns (is_provable, inference_steps)
        
        Query format: "NOT pit_2_1" to ask "Is pit_2_1 definitely not there?"
        """
        self.inference_steps = 0
        
        # Add negation of query to KB
        negated_query = self.negate(query)
        query_clause = Clause([negated_query])
        
        # Keep track of clauses we've seen
        clauses_to_resolve = set(self.clauses)
        clauses_to_resolve.add(query_clause)
        
        new_clauses = True
        
        while new_clauses:
            new_clauses = False
            clauses_list = list(clauses_to_resolve)
            
            # Try to resolve all pairs
            for i in range(len(clauses_list)):
                for j in range(i + 1, len(clauses_list)):
                    c1 = clauses_list[i]
                    c2 = clauses_list[j]
                    
                    # Find complementary literals
                    for literal in c1.literals:
                        neg_literal = self.negate(literal)
                        if neg_literal in c2.literals:
                            # Can resolve!
                            self.inference_steps += 1
                            resolvent = self.resolve(c1, c2, literal)
                            
                            # Empty clause = contradiction = proof!
                            if len(resolvent.literals) == 0:
                                return (True, self.inference_steps)
                            
                            # Add new clause if not already there
                            if resolvent not in clauses_to_resolve:
                                clauses_to_resolve.add(resolvent)
                                new_clauses = True
        
        # No contradiction found - cannot prove
        return (False, self.inference_steps)
    
    def reset(self):
        """Clear the knowledge base"""
        self.clauses = set()
        self.inference_steps = 0
    
    def get_stats(self):
        """Get KB statistics"""
        return {
            "num_clauses": len(self.clauses),
            "inference_steps": self.inference_steps
        }
