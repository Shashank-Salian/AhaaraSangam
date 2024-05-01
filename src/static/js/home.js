/** @type {HTMLSelectElement} */
const filterStateInput = document.querySelector("form select[name='state']");
/** @type {HTMLSelectElement} */
const filterCityInput = document.querySelector("form select[name='city']");
/** @type {HTMLFormElement} */
const filterForm = document.querySelector("form");

/**
 *
 * @param {Event} e
 */
function onFilterChange(e) {
  setTimeout(() => {
    filterForm.submit();
  }, 100);
}

/**
 * @param {string} stateIso
 * @param {HTMLSelectElement} cityInput
 */
function afterCitiesFetched(stateIso, cityInput) {
  const urlQuery = new URLSearchParams(location.search);
  const city = urlQuery.get("city");

  /** @type {HTMLOptionElement | null} */
  const selectedCity = cityInput.querySelector(`option[value="${city}"]`);
  if (selectedCity) {
    selectedCity.selected = true;
    return;
  }

  const option = document.createElement("option");
  option.value = city;
  option.text = city;
  cityInput.appendChild(option);
  option.selected = true;
}

filterStateInput.addEventListener("change", onFilterChange);
filterCityInput.addEventListener("change", onFilterChange);
