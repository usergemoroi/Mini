import httpx
import hashlib
import hmac
import config
from typing import Dict, Optional
import json
import logging

logger = logging.getLogger(__name__)

class CryptoBotAPI:
    """Wrapper for CryptoBot API"""
    
    def __init__(self, api_token: str = None):
        self.api_token = api_token or config.CRYPTOBOT_API_TOKEN
        self.base_url = config.CRYPTOBOT_API_URL
    
    async def create_invoice(
        self,
        amount: float,
        currency: str,
        description: str,
        payload: str = None
    ) -> Dict:
        """Create a payment invoice"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/createInvoice",
                    headers={
                        "Crypto-Pay-API-Token": self.api_token
                    },
                    json={
                        "asset": currency,
                        "amount": str(amount),
                        "description": description,
                        "payload": payload or ""
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('ok'):
                    return {
                        'success': True,
                        'invoice_id': data['result']['invoice_id'],
                        'pay_url': data['result']['pay_url'],
                        'amount': data['result']['amount'],
                        'currency': data['result']['asset']
                    }
                else:
                    return {
                        'success': False,
                        'error': data.get('error', 'Unknown error')
                    }
        except Exception as e:
            logger.error(f"Error creating CryptoBot invoice: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_invoice(self, invoice_id: str) -> Dict:
        """Get invoice status"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/getInvoice",
                    headers={
                        "Crypto-Pay-API-Token": self.api_token
                    },
                    params={
                        "invoice_id": invoice_id
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('ok'):
                    invoice = data['result']
                    status_map = {
                        'active': 'pending',
                        'paid': 'completed',
                        'expired': 'failed',
                        'failed': 'failed'
                    }
                    return {
                        'success': True,
                        'invoice_id': invoice['invoice_id'],
                        'status': status_map.get(invoice['status'], invoice['status']),
                        'amount': float(invoice['amount']),
                        'currency': invoice['asset'],
                        'pay_url': invoice.get('pay_url')
                    }
                else:
                    return {
                        'success': False,
                        'error': data.get('error', 'Unknown error')
                    }
        except Exception as e:
            logger.error(f"Error getting CryptoBot invoice: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_currencies(self) -> Dict:
        """Get available currencies"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/getCurrencies",
                    headers={
                        "Crypto-Pay-API-Token": self.api_token
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('ok'):
                    return {
                        'success': True,
                        'currencies': data['result']
                    }
                else:
                    return {
                        'success': False,
                        'error': data.get('error', 'Unknown error')
                    }
        except Exception as e:
            logger.error(f"Error getting CryptoBot currencies: {e}")
            return {'success': False, 'error': str(e)}
    
    async def get_balance(self) -> Dict:
        """Get wallet balance"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/getBalance",
                    headers={
                        "Crypto-Pay-API-Token": self.api_token
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                if data.get('ok'):
                    return {
                        'success': True,
                        'balance': data['result']
                    }
                else:
                    return {
                        'success': False,
                        'error': data.get('error', 'Unknown error')
                    }
        except Exception as e:
            logger.error(f"Error getting CryptoBot balance: {e}")
            return {'success': False, 'error': str(e)}
