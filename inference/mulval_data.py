from __future__ import absolute_import


import os, sys, time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from service.client import Client
"""Gets the graph that will be translated into MulVAL predicates"""
class TranslatorBuilder():
    def __init__(self, client):
        self.data = None
        self.client = client

    def from_client_data(self):
        try:
            self.data = self.client.get("/graph")
        except Exception as e:
            return self
        return self

    def build(self, mulval_translator):
        mulval_translator.data = self.data
        return mulval_translator
