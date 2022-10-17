import "./App.css";
import axios from "axios";
import React, { useEffect, useState } from "react";
import Button from "./UI/Button";
import Card from "./UI/Card";

function App() {
  const [vehicles, setVehicles] = useState([]);
  const [filterText, setFilterText] = useState("");
  const [onlyAvailable, setOnlyAvailable] = React.useState(false);

  const getVehicles = async () => {
    const { data } = await axios("/vehicles/list");
    console.log("data!!!!!!!!", data);
    setVehicles(data);
  };
  const occupyVehicle = async (vehicleId) => {
    const { ifOccupy } = await axios.post(`/vehicles/${vehicleId}/occupy/`);
    console.log("occupy Vehicle", ifOccupy);
    getVehicles();
  };
  const releaseVehicle = async (vehicleId) => {
    const { ifORelease } = await axios.post(`/vehicles/${vehicleId}/release/`);
    getVehicles();

    console.log("release Vehicle");
  };

  const getHistory = async (plate) => {
    const res = await axios.get(`/vehicles/${plate}/history/`);
    const historyTasks = res.data;
    alert(JSON.stringify(historyTasks));
  };

  const renderVehicles = (_vehicles) => {
    return _vehicles
      .filter(
        (vehicle) =>
          (vehicle.license_plate_number
            .toLowerCase()
            .includes(filterText.toLowerCase()) ||
            vehicle.manufacturer
              .toLowerCase()
              .includes(filterText.toLowerCase())) &&
          (onlyAvailable ? vehicle.is_available : true)
      )
      .map((v) => {
        return (
          <div className="vehicles-wrapper">
            <Card>
              <div>
                <div className="header-wrapper">
                  <p
                    className={
                      v.is_available ? "available-color" : "unavailable-color"
                    }
                  >
                    {v.is_available ? "available" : "unavailable"}
                    {!v.is_available && (
                      <span>(owned by : {v.owner_username})</span>
                    )}
                  </p>
                  <Button onClick={() => getHistory(v.license_plate_number)}>
                    History
                  </Button>
                </div>

                <p>
                  <span className="bold-text">manufacturer:</span>
                  {v.manufacturer}
                </p>
                <p>
                  <span className="bold-text">license plate number:</span>
                  {v.license_plate_number}
                </p>
              </div>

              <div className="buttons-wrapper">
                <div className="occupy-wrapper">
                  <Button
                    className={
                      "button " +
                      (v.is_available ? "available" : "not-available")
                    }
                    onClick={() => occupyVehicle(v.id)}
                  >
                    Occupy
                  </Button>

                  <span
                    className={
                      !v.is_available ? "not-available-text" : "text-disable"
                    }
                  >
                    Vehicle is not available
                  </span>
                </div>
                <div className="release-wrapper">
                  <Button
                    className={
                      "button " +
                      (!v.is_available && v.is_owned_by_me
                        ? "available"
                        : "not-available-and-owner")
                    }
                    onClick={() => releaseVehicle(v.id)}
                  >
                    Release
                  </Button>
                </div>
              </div>
            </Card>
          </div>
        );
      });
  };

  useEffect(() => {
    getVehicles();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h2>Vehicles list </h2>
        <div className="filter-wrapper">
          <input
            type="text"
            placeholder="Search..."
            onChange={(e) => setFilterText(e.target.value)}
          ></input>
          <label>
            <input
              type="checkbox"
              defaultChecked={onlyAvailable}
              onChange={() => setOnlyAvailable(!onlyAvailable)}
            />
            Show only available
          </label>
        </div>
      </header>
      {renderVehicles(vehicles)}
    </div>
  );
}

export default App;
