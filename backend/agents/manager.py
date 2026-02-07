from pydantic import BaseModel, Field
from typing import List, Optional
from base_res_class import BaseAgentResult
import asyncio
from dedalus_labs import AsyncDedalus, DedalusRunner
import os
from dotenv import load_dotenv, find_dotenv


from claim_check import claim_agent, claim_result
from bias import bias_check_agent, BiasCheckResult
from citation_check import citation_check_agent, CitationResult
from base_res_class import BaseAgentResult
from author_org_check import author_check_agent, AuthorResult
from evidence_check import evidence_check_agent, EvidenceResult
from usefullness_check import usefulness_check_agent, UsefulnessResult
from AI_check import ai_check_agent, AICheckResult

# Variables
load_dotenv(find_dotenv())
dedalus_api_key = os.getenv('DEDALUS_API_KEY')

async def manager_agent(client, url: str, input_text: str, topic:str) -> List[BaseAgentResult]:
    """Manager agent to coordinate multiple analysis agents"""
    # Run claim check agent
    claim_res, citation_res, bias_res, author_res, ai_res  = await asyncio.gather(
        claim_agent(client, url),
        citation_check_agent(client, url),
        bias_check_agent(client, url),
        author_check_agent(client, url),
        ai_check_agent(client, url)
    )
    
    ev_res, usefulness_res = await asyncio.gather(
        evidence_check_agent(client, url, claim_res.central_claim),
        usefulness_check_agent(client, url, topic)
    )
    
    return (claim_res, citation_res, bias_res, author_res, ev_res, usefulness_res, ai_res)


async def main():
    # url = input("Provide URL to analyze: ")
    client = AsyncDedalus(api_key=dedalus_api_key)
    
    claim_res, citation_res, bias_res, author_res, ev_res, usefulness_res, ai_res  = await manager_agent(client, url= None, input_text = None, topic = "Indian")  

    
    # Print results in clean format
    print("Manager Agent Results")
    print(f"\n📍 Central Claim: {claim_res.central_claim}")
    print(f"n📍 Claim Analysis: {claim_res.overall_score}")
    print(f"n📍 Citation Analysis: {citation_res.overall_score}")
    print(f"n📍 Bias Analysis: {bias_res.overall_score}")
    print(f"n📍 Author/Organization Analysis: {author_res.overall_score}")
    print(f"n📍 Evidence Analysis: {ev_res.overall_score}")
    print(f"n📍 Usefulness Analysis: {usefulness_res.overall_score}")
    print(f"n📍 AI Detection Analysis: {ai_res.overall_score}")



if __name__ == "__main__":
    print("Running manager.py")
    asyncio.run(main())
   