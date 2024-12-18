import React, { useEffect, useState } from "react";

const App = () => {
  const [data, setData] = useState(null);
  const [filteredData, setFilteredData] = useState([]);

  // Fetch data from the Flask backend when the component mounts
  useEffect(() => {
    fetch("/api/data")
      .then((response) => response.json())
      .then((jsonData) => setData(jsonData))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  // Function to filter applications based on criteria
  const filterApplications = (activeStatus = null, nameContains = "") => {
    if (!data) return;

    const result = data.nodes
      .map((node) => {
        // Filter applications within each node based on criteria
        const filteredApps = node.applications.filter((app) => {
          const isActiveMatch = activeStatus === null || app.active === activeStatus;
          const isNameMatch = nameContains === "" || app.name.includes(nameContains);
          return isActiveMatch && isNameMatch;
        });

        // Return node with filtered applications if any match
        if (filteredApps.length > 0) {
          return {
            hostname: node.hostname,
            applications: filteredApps,
          };
        }
        return null;
      })
      .filter((node) => node !== null); // Remove nodes with no matching applications

    setFilteredData(result);
  };

  return (
    <div>
      <h1>Filtered Applications</h1>

      <button onClick={() => filterApplications(true, "gateway")}>
        Show Active Apps with "gateway" in Name
      </button>
      <button onClick={() => filterApplications(false)}>
        Show Inactive Apps
      </button>
      <button onClick={() => filterApplications()}>
        Show All Apps
      </button>

      <h2>Filtered Results:</h2>
      <pre>{JSON.stringify(filteredData, null, 2)}</pre>
    </div>
  );
};

export default App;