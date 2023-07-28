#Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib


# Define a new Python data class named `Record`.
# Add the `@dataclass` decorator immediately before the `Record` class definition.
# Add attributes `sender` of type `str`, `receiver` of type `str`, and `amount` of type `float` to the `Record` class.
@dataclass
class Record:
    sender: str
    receiver: str
    amount: float

    # In the `Block` class, rename the `data` attribute to `record`.
# Set the data type of the `record` attribute to `Record`.
@dataclass
class Block:
    record: Record
    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    # Modify the `hash_block` method to use `self.record` instead of `self.data`.
    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()
    
@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Wining Hash", calculated_hash)
        return block

    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

################################################################################
# Streamlit Code

# Adds the cache decorator for Streamlit


@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])


st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()
    
    
    # Delete the `input_data` variable from the Streamlit interface.
# Add input areas to capture values for `sender`, `receiver`, and `amount` from the user.
# Update the `new_block` functionality to use the user-provided inputs and create a new `Record` object.
sender_input = st.text_input("Sender")
receiver_input = st.text_input("Receiver")
amount_input = st.number_input("Amount")

if st.button("Add Block"):
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # Create a new `Record` object using the user-provided inputs
    new_record = Record(sender=sender_input, receiver=receiver_input, amount=amount_input)

    # Update `new_block` to use the new `Record` object
    new_block = Block(record=new_record, creator_id=42, prev_hash=prev_block_hash)

    pychain.add_block(new_block)
    st.balloons()
    
    # Streamlit Code (continues)

@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])

@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    # The rest of the PyChain class methods (proof_of_work, is_valid, add_block)

# Define the pychain variable and initialize it with the setup() function
pychain = setup()

# Streamlit Code (continues)

pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

if st.button("Validate Chain"):
    st.write(pychain.is_valid())

