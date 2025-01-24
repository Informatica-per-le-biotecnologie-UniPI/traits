import copy
from typing import Optional

from functools import reduce
from random import choice, choices

from more_itertools import flatten


class Trait:
    """Definisce il valore di un carattere, e.g., blu per la Characteristic colore occhi."""
    def __init__(self, name: str, optional_value: Optional[object] = None,
                 dominance: Optional[float] = None,
                 coding_sequences: Optional[set[str]] = None):
        if dominance < 0 or dominance > 1:
            raise ValueError(f"Expected dominance in [0, 1], {dominance} found")


        self.name = name
        self.optional_value = optional_value
        self.dominance = dominance

        if coding_sequences is None or len(coding_sequences) == 0:
            raise ValueError(f"Provide a non-empty set of coding sequences!")
        else:
            lengths = [len(coding_sequence) for coding_sequence in coding_sequences]
            if len(set(lengths)) != 1:
                raise ValueError(f"Found encoding sequences of different lengths: {lengths}")
            
            self.coding_sequences = coding_sequences
            self.length = lengths[0]
    
    def __str__(self) -> str:
        return f"Trait {self.name} with dominance {self.dominance} and coding sequences {self.coding_sequences}"
    
    def __eq__(self, other):
        if isinstance(other, Trait):
            return self.name == other.name and\
                   self.dominance == other.dominance and\
                   self.coding_sequences == other.coding_sequences
        
        return False

    def __hash__(self):
        return hash(self.name) + hash(reduce(lambda a, b: a + b, self.coding_sequences, ""))
    
    def __len__(self):
        return self.length

    def __deepcopy__(self):
        return Trait(
            self.name,
            copy.deepcopy(self.optional_value),
            self.dominance,
            coding_sequences={sequence for sequence in self.coding_sequences}
        )


class Characteristic:
    """Definisce una caratteristica di un organismo, i.e., una proprieta' dello stesso, e.g. colore occhi."""
    def __init__(self, name: str, starting_position: int, traits: list[Trait]):
        """
        Params:
            name: Name assigned to the characteristic, e.g., "eye color"
            traits: List of traits
        """
        if sum([trait.dominance for trait in traits]) != 1:
            raise ValueError(f"Probabilities should sum to 1, but sum to {sum([value.dominance for value in traits])}")
        
        all_names = [trait.name for trait in traits]
        if len(all_names) != len(set(all_names)):
            raise ValueError(f"Found trait values with the same name!")

        all_sequences = list(flatten([trait.coding_sequences for trait in traits]))
        if len(all_sequences) != len(set(all_sequences)):
            raise ValueError(f"Found a sequence that encodes for multiple values!")
        
        all_lengths = [len(trait_value) for trait_value in traits]
        if len(set(all_lengths)) != 1:
            raise ValueError(f"Found values with different length traits: {set(all_lengths)}")

        if starting_position < 0:
            raise ValueError(f"Starting position negativa: {starting_position}")

        self.name = name
        self.traits = traits
        self.starting_position = starting_position

    def __eq__(self, other):
        return isinstance(other, Characteristic)\
            and self.name == other.name\
            and self.traits == other.traits\
            and self.starting_position == other.starting_position

    def __getitem__(self, key: str):
        for trait in self.traits:
            if trait.name == key:
                return trait
        
        raise IndexError(f"Value {key} not found")

    def __len__(self):
        return len(self.traits)

    def __str__(self):
        base = f"Trait {self.name} ({self.starting_position}) with phenotype:\n"
        for trait in self.traits:
            base += f"\t{str(trait)}\n"
        
        return base
    
    def __contains__(self, key):
        if isinstance(key, str):
            for trait in self.traits:
                if key == trait.name:
                    return True
            
            return False
        
        elif isinstance(key, Trait):
            for trait in self.traits:
                if trait == key:
                    return True
            
            return False

        else:
            return False

    def __hash__(self):
        return hash(self.name) + hash(self.starting_position) + hash(self.traits)

    def __deepcopy__(self):
        return Characteristic(
            name=self.name,
            traits=[copy.deepcopy(trait) for trait in self.traits],
            starting_position=self.starting_position
        )

    def search_genome(self, genome: str) -> Optional[Trait]:
        """What value does the given `genome` encode? None if no value is encoded.
        
        Params:
            genome: The genome to search.
        
        Returns:
            The trait value if there exists a trait encoded with the given genome, None otherwise.
        """
        for trait_value in self.traits:
            if genome in trait_value.coding_sequences:
                return trait_value
        
        return None


    def random_value(self, weighted: bool = False) -> Trait:
        """Get a random of the possible traits for this Characteristic.
        
        Params:
            weighted: True to sample according to dominance, False otherwise. Defaults to False.
        
        Returns:
            A random trait.
        """
        if weighted:
            return choices(self.traits, weights=[t.dominance for t in self.traits], k=1)[0]
        else:
            return choice(self.traits)
