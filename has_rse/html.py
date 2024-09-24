import json
from typing import List, Dict
from time import strftime


def generate_html(university_data: List[Dict], out_path: str) -> None:
    """Generates an HTML file listing R1 universities and highlighting those with RSE groups.

    Args:
        university_data: A list of dictionaries containing university data.
        out_path: Path to save the generated HTML file.
    """

    total_universities = len(university_data)
    universities_with_rse = sum(university["has_rse"] for university in university_data)
    last_checked_date = strftime("%Y-%m-%d")

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
  <title>R1 Universities with RSE Groups</title>
  <link rel="stylesheet" href="style.css">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/awesomplete@1.1.5/awesomplete.css" />
</head>
<body>
  <div class="container">
    <div class="centered-content">
      <h1>R1 Universities with RSE Groups</h1>
      <p>As of {last_checked_date}, <strong>{universities_with_rse} out of {total_universities}</strong> R1 universities
         appear to have RSE groups based on search results. If you find errors, please, open an <a href=https://github.com/Sbozzolo/has_rse/issues>issue</a>. See code  <a href=https://github.com/Sbozzolo/has_rse>here</a>. </p>

      <input type="text" id="searchInput" placeholder="Search universities..." class="awesomplete" list="universityList">
      <datalist id="universityList">
      </datalist>

      <table class="styled-table" id="universityTable">
        <thead>
          <tr>
            <th>University</th>
            <th>RSE Group</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
"""

    for university in university_data:
        rse_status = "✅" if university["has_rse"] else "❌"
        link = university.get("link")
        link_html = f'<a href="{link}" target="_blank">Link</a>' if link else ""
        html_content += f"""
        <tr>
           <td>{university["name"]}</td>
           <td style="text-align: center;">{rse_status}</td>
           <td>{link_html}</td>
        </tr>
        """

    html_content += """
        </tbody>
      </table>

      <div class="info">
        <h2 onclick="toggleInfo()">How this list was generated: <span id="info-arrow">▼</span></h2>
        <div id="info-content" style="display: none;">
          <ol>
            <li>For each R1 university, a search query was performed on DuckDuckGo
                using the university name and "research software engineering" related terms.</li>
            <li>The search results were filtered to include only those from .edu domains.</li>
            <li>If a search result contained keywords related to RSE groups (e.g., "research
                software engineer", "RSE team"), the university was marked as having an RSE group.</li>
            <li>The "Link" column provides a link to the first search result that indicated
                the presence of an RSE group (if found).</li>
          </ol>
          <p><strong>Note:</strong> This is an automated process and the results might not be perfectly accurate.
             It is recommended to verify the information by visiting the university's website.</p>
        </div>
      </div>
    </div>
  </div>

      <script src="https://cdn.jsdelivr.net/npm/awesomplete@1.1.5/awesomplete.min.js"></script>
      <script>
        const searchInput = document.getElementById('searchInput');
        const table = document.getElementById('universityTable');
        const rows = table.querySelectorAll('tbody tr');
        const universityNames = [];

        rows.forEach(row => {
          universityNames.push(row.cells[0].textContent);
        });

        searchInput.addEventListener('keyup', () => {
          const filter = searchInput.value.toLowerCase();
          rows.forEach(row => {
            const universityName = row.cells[0].textContent.toLowerCase();
            if (universityName.includes(filter)) {
              row.style.display = '';
            } else {
              row.style.display = 'none';
            }
          });
        });

        // Autocomplete with Awesomplete
        new Awesomplete(searchInput, {
          list: universityNames,
          minChars: 1, // Start suggesting after 1 character
          autoSelect: true // Auto-select the first suggestion
        });

        // JavaScript to toggle the info section
        function toggleInfo() {
          var infoContent = document.getElementById("info-content");
          var arrow = document.getElementById("info-arrow");
          if (infoContent.style.display === "none") {
            infoContent.style.display = "block";
            arrow.textContent = "▲"; // Change arrow to up
          } else {
            infoContent.style.display = "none";
            arrow.textContent = "▼"; // Change arrow to down
          }
        }
      </script>
    </body>
    </html>
    """

    with open(out_path, "w") as f:
        f.write(html_content)
