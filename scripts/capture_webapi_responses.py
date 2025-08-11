#!/usr/bin/env python3
"""
Capture WebAPI responses for testing.

This script collects real responses from the Atlas demo WebAPI
and saves them as JSON files for use in testing our Pydantic models.

Run with: poetry run python scripts/capture_webapi_responses.py
"""

import json
import time
from pathlib import Path
from typing import Any

import requests


class WebApiResponseCapture:
    """Captures and saves WebAPI responses for testing."""

    def __init__(self, base_url: str = "https://atlas-demo.ohdsi.org/WebAPI"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "OHDSI-Cohort-Schemas-TestData-Collector/1.0"
        })

    def save_response(self, endpoint: str, filename: str, data: Any) -> None:
        """Save response data to a JSON file."""
        output_dir = Path("tests/webapi_responses/atlas-demo")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / filename
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Saved {endpoint} → {output_file}")

    def get_json(self, endpoint: str) -> Any:
        """Make a GET request and return JSON response."""
        url = f"{self.base_url}{endpoint}"
        print(f"🔍 Fetching {endpoint}...")
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching {endpoint}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error for {endpoint}: {e}")
            return None

    def capture_cohort_definitions(self) -> None:
        """Capture cohort definition responses."""
        print("\\n📋 Capturing cohort definitions...")
        
        # List all cohort definitions
        cohorts_list = self.get_json("/cohortdefinition")
        if cohorts_list:
            self.save_response("/cohortdefinition", "cohortdefinition/list_response.json", cohorts_list)
            
            # Get details for first few cohorts
            for i, cohort in enumerate(cohorts_list[:3]):
                cohort_id = cohort.get("id")
                if cohort_id:
                    time.sleep(0.5)  # Be nice to the API
                    
                    # Single cohort definition
                    cohort_detail = self.get_json(f"/cohortdefinition/{cohort_id}")
                    if cohort_detail:
                        self.save_response(
                            f"/cohortdefinition/{cohort_id}", 
                            f"cohortdefinition/cohort_{cohort_id}.json", 
                            cohort_detail
                        )
                    
                    # Cohort expression
                    cohort_expression = self.get_json(f"/cohortdefinition/{cohort_id}/expression")
                    if cohort_expression:
                        self.save_response(
                            f"/cohortdefinition/{cohort_id}/expression", 
                            f"cohortdefinition/expression_{cohort_id}.json", 
                            cohort_expression
                        )
                    
                    # Generation info (if available)
                    gen_info = self.get_json(f"/cohortdefinition/{cohort_id}/info")
                    if gen_info:
                        self.save_response(
                            f"/cohortdefinition/{cohort_id}/info", 
                            f"cohortdefinition/info_{cohort_id}.json", 
                            gen_info
                        )

    def capture_concept_sets(self) -> None:
        """Capture concept set responses."""
        print("\\n🎯 Capturing concept sets...")
        
        # List all concept sets
        conceptsets_list = self.get_json("/conceptset")
        if conceptsets_list:
            self.save_response("/conceptset", "conceptset/list_response.json", conceptsets_list)
            
            # Get details for first few concept sets
            for i, cs in enumerate(conceptsets_list[:3]):
                cs_id = cs.get("id")
                if cs_id:
                    time.sleep(0.5)  # Be nice to the API
                    
                    # Single concept set
                    cs_detail = self.get_json(f"/conceptset/{cs_id}")
                    if cs_detail:
                        self.save_response(
                            f"/conceptset/{cs_id}", 
                            f"conceptset/conceptset_{cs_id}.json", 
                            cs_detail
                        )
                    
                    # Concept set expression
                    cs_expression = self.get_json(f"/conceptset/{cs_id}/expression")
                    if cs_expression:
                        self.save_response(
                            f"/conceptset/{cs_id}/expression", 
                            f"conceptset/expression_{cs_id}.json", 
                            cs_expression
                        )
                    
                    # Resolved items
                    cs_items = self.get_json(f"/conceptset/{cs_id}/items")
                    if cs_items:
                        self.save_response(
                            f"/conceptset/{cs_id}/items", 
                            f"conceptset/items_{cs_id}.json", 
                            cs_items
                        )

    def capture_vocabulary(self) -> None:
        """Capture vocabulary/concept responses."""
        print("\\n📖 Capturing vocabulary responses...")
        
        # Search for common terms
        search_terms = ["diabetes", "cardiovascular", "metformin"]
        for term in search_terms:
            time.sleep(0.5)
            search_results = self.get_json(f"/vocabulary/search?query={term}")
            if search_results:
                self.save_response(
                    f"/vocabulary/search?query={term}", 
                    f"vocabulary/search_{term}.json", 
                    search_results
                )
        
        # Get details for specific concepts (common ones we know exist)
        concept_ids = [201820, 4329847, 1593467]  # Diabetes, MI, Dupilumab
        for concept_id in concept_ids:
            time.sleep(0.5)
            
            # Single concept
            concept = self.get_json(f"/vocabulary/concept/{concept_id}")
            if concept:
                self.save_response(
                    f"/vocabulary/concept/{concept_id}", 
                    f"vocabulary/concept_{concept_id}.json", 
                    concept
                )
            
            # Descendants
            descendants = self.get_json(f"/vocabulary/concept/{concept_id}/descendants")
            if descendants:
                self.save_response(
                    f"/vocabulary/concept/{concept_id}/descendants", 
                    f"vocabulary/descendants_{concept_id}.json", 
                    descendants
                )
            
            # Ancestors
            ancestors = self.get_json(f"/vocabulary/concept/{concept_id}/ancestors")
            if ancestors:
                self.save_response(
                    f"/vocabulary/concept/{concept_id}/ancestors", 
                    f"vocabulary/ancestors_{concept_id}.json", 
                    ancestors
                )

    def capture_sources(self) -> None:
        """Capture source information."""
        print("\\n🏥 Capturing sources...")
        
        sources = self.get_json("/source/sources")
        if sources:
            self.save_response("/source/sources", "source/sources_list.json", sources)

    def capture_info(self) -> None:
        """Capture WebAPI info."""
        print("\\n ℹ️ Capturing WebAPI info...")
        
        info = self.get_json("/info")
        if info:
            self.save_response("/info", "info/version_info.json", info)

    def capture_all(self) -> None:
        """Capture responses from all priority endpoints."""
        print(f"🚀 Starting WebAPI response capture from {self.base_url}")
        print("=" * 60)
        
        try:
            self.capture_info()
            self.capture_sources()
            self.capture_vocabulary()
            self.capture_concept_sets()
            self.capture_cohort_definitions()
            
            print("\\n" + "=" * 60)
            print("✅ WebAPI response capture complete!")
            print("📁 Responses saved to: tests/webapi_responses/atlas-demo/")
            
        except KeyboardInterrupt:
            print("\\n⚠️ Capture interrupted by user")
        except Exception as e:
            print(f"\\n❌ Unexpected error: {e}")


def main():
    """Main entry point."""
    capturer = WebApiResponseCapture()
    capturer.capture_all()


if __name__ == "__main__":
    main()
