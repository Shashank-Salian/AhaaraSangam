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
  const response = await fetch(`/api/cities/${stateIso}`);
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

stateInput.addEventListener("change", async (e) => {
  console.log(e.target.value);
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
  } catch (e) {
    console.error(e);
    alert("Something went wrong. Please try again later.");
  }
});
