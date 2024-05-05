/** @type {HTMLSelectElement} */
const stateInput = document.querySelector("form select[name='state']");
/** @type {HTMLSelectElement} */
const cityInput = document.querySelector("form select[name='city']");

/**
 *
 * @param {string} stateIso
 * @returns {Promise<{id: number,name: string}[]>}
 */
async function getCitiesOfStates(stateIso) {
  const response = await fetch(`/api/cities/${stateIso}/`);
  if (response.status !== 200) {
    throw new Error("Something went wrong. Please try again later.");
  }
  const data = await response.json();
  return data;
}

/**
 *
 * @param {{id: number,name: string}[]} cities
 * @returns {{id: number,name: string}[]}
 */
function sortCities(cities) {
  return cities.sort((a, b) => a.name.localeCompare(b.name));
}

function clearCities() {
  console.log(cityInput.selectedOptions);
  while (cityInput.firstChild) {
    cityInput.removeChild(cityInput.firstChild);
  }

  const option = document.createElement("option");
  option.value = "0";
  option.text = "Select City";
  cityInput.appendChild(option);
}

/**
 *
 * @param {Event} e
 */
async function onStateChange(e) {
  clearCities();
  if (e.target.value == "0") {
    return;
  }

  let stateIso = e.target.value.split(";")[1];

  try {
    let cities = await getCitiesOfStates(stateIso);
    cities = sortCities(cities);

    for (const city of cities) {
      const option = document.createElement("option");
      option.value = city.name;
      option.text = city.name;
      cityInput.appendChild(option);
    }
  } catch (err) {
    console.error(err);
    alert(
      "Something went wrong while fetching the cities. Please try again later."
    );
  }

  if (typeof afterCitiesFetched !== "undefined") {
    afterCitiesFetched(stateIso, cityInput);
  }
}

stateInput.addEventListener("change", onStateChange);

const selectedOption = stateInput.selectedOptions[0];

if (selectedOption.value != "0") {
  onStateChange({ target: selectedOption });
}
