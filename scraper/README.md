# Web Scraper

## Usage
```bash
python -m scraper
```

## Environment Variables
| Name | Description | Default |
| ---- | ----------- | ------- |
| `VOTE_SCRAPER_HOUSE_URL` | URL prefix for House of Representatives vote XML | https://clerk.house.gov/evs |
| `VOTE_SCRAPER_SENATE_MEMBER_URL` | URL of senate contact information XML | https://www.senate.gov/general/contact_information/senators_cfm.xml |
| `VOTE_SCRAPER_SENATE_URL` | URL for senate vote results XML | https://www.senate.gov/legislative/LIS/roll_call_votes |
| `VOTE_SCRAPER_CRAWL_DELAY_SECONDS` | Time to wait between each HTTP request | 0.4 |
| `VOTE_SCRAPER_NEO4J_URI` | URI used to connect to database server | neo4j://localhost:7687 |
| `VOTE_SCRAPER_NEO4J_USERNAME` | Username to connect to database with | neo4j |
| `VOTE_SCRAPER_NEO4J_PASSWORD` | Password to connect to database with | NONE |
| `VOTE_SCRAPER_RESUME_YEAR` | If database is empty, year to start scraping house votes at | 2025 |
| `VOTE_SCRAPER_RESUME_CONGRESS` | If database is empty, congress to start scraping senate votes at | 119 |
| `VOTE_SCRAPER_LOG_LEVEL` | Default log level. Should be `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL` | `INFO` |

## Requirements
- neo4j
- unidecode
