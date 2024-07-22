from typing import Optional
from langchain_mistralai import ChatMistralAI
from langchain_core.pydantic_v1 import BaseModel, Field

class Expense(BaseModel):
        """Information about a transaction made on any Card"""
        amount: Optional[str] = Field(title="expense", description="Expense made on the transaction, extract amount, if ammount is in whole number or floating point number extract only amount value and nothing else")
        merchant: Optional[str] = Field(title="merchant", description="Merchant name whom the transaction has been made")
        currency: Optional[str] = Field(title="currency", description="currency of the transaction")

        def serialize(self):
                return {
                'amount': self.amount,
                'merchant': self.merchant,
                'currency': self.currency,
                }