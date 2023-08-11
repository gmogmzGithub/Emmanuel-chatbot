import os
import streamlit as st


class PaymentHandler:
    def __init__(self, directory_path="./embeddings/"):
        self.directory_path = directory_path

    def count_pkl_files(self):
        return len([f for f in os.listdir(self.directory_path) if f.endswith(".pkl")])

    def display_payment_button(self):
        stripe_button_code = """
        <script async src="https://js.stripe.com/v3/buy-button.js"></script>
        <stripe-buy-button
          buy-button-id="buy_btn_1NdPiTGdeQC5XJgp58dd2Xuw"
          publishable-key="pk_live_51NcJEcGdeQC5XJgphWhG8ngtAseFKNyVdJhfIZoxtzcm1UMeFbSMrLO8xiVCLEouUplxRycu5vtdee045DIf2olr00EGsQE7I7">
        </stripe-buy-button>
        """
        st.markdown(stripe_button_code, unsafe_allow_html=True)
        st.write("You have reached the limit of 3 processed files. Please purchase additional processing.")
