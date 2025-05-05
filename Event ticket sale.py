import streamlit as st
import hashlib
import datetime

# Define a Block
class TicketBlock:
    def __init__(self, event_name, buyer_name, seat_no, price, previous_hash=''):
        self.timestamp = datetime.datetime.utcnow().isoformat()
        self.event_name = event_name
        self.buyer_name = buyer_name
        self.seat_no = seat_no
        self.price = price
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        data = self.timestamp + self.event_name + self.buyer_name + self.seat_no + str(self.price) + self.previous_hash
        return hashlib.sha256(data.encode()).hexdigest()

# Blockchain to store ticket sales
class TicketBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return TicketBlock("Genesis Event", "None", "0", 0, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_ticket_sale(self, event_name, buyer_name, seat_no, price):
        previous_hash = self.get_latest_block().hash
        new_block = TicketBlock(event_name, buyer_name, seat_no, price, previous_hash)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

# Initialize blockchain in session state
if "ticket_chain" not in st.session_state:
    st.session_state.ticket_chain = TicketBlockchain()

st.title("🎟️ Blockchain-Based Ticketing System")

# Ticket Sale Form
with st.form("ticket_form"):
    st.subheader("Enter Ticket Sale Information")
    event_name = st.text_input("Event Name")
    buyer_name = st.text_input("Buyer Name")
    seat_no = st.text_input("Seat Number")
    price = st.number_input("Ticket Price", min_value=0.0, format="%.2f")

    submitted = st.form_submit_button("Add Ticket")
    if submitted:
        if event_name and buyer_name and seat_no and price > 0:
            st.session_state.ticket_chain.add_ticket_sale(event_name, buyer_name, seat_no, price)
            st.success("✅ Ticket added successfully!")
        else:
            st.error("⚠️ Please fill in all fields correctly.")

# Display the blockchain
st.subheader("📜 Blockchain Ledger")
for i, block in enumerate(st.session_state.ticket_chain.chain):
    with st.expander(f"Block {i}"):
        st.write(f"**Event:** {block.event_name}")
        st.write(f"**Buyer:** {block.buyer_name}")
        st.write(f"**Seat No:** {block.seat_no}")
        st.write(f"**Price:** ₹{block.price}")
        st.write(f"**Timestamp:** {block.timestamp}")
        st.code(f"Previous Hash: {block.previous_hash}")
        st.code(f"Hash: {block.hash}")

# Chain validation
if st.session_state.ticket_chain.is_chain_valid():
    st.success("✅ Blockchain is valid.")
else:
    st.error("❌ Blockchain has been tampered!")

