# team_productivity_report
Team productivity report will be generated for a given project - JSON results

## How to run?
python3 lit_report.py <sentry_project (string)>, <start_date (datetime)>, <end_date (datetime)>, <top_n_issues (int)>, <api_key (string)>

Example:
python3 lit_report.py react 9/1/2024 9/3/2024 3 46e38b1def35f16d66bdaec0d438d82ba98de5d2a0a647f0fddf71d2d6cb973d

## Output
```json
Project = {
  name:
  teams: [
    team = {
      name:  
      numberOfIssues: 
      numberOfevents:
      topIssues: [
        {"issue_id":1, "title":"a", count:150},
        {"issue_id":2, "title":"b", count:100},
        {"issue_id":3, "title":"c", count:40},
      ];
   }
}
```
