window.mountChainlitWidget({
  chainlitServer: "http://localhost:8000",
});

window.addEventListener("chainlit-call-fn", (e) => {
  const { name, args, callback } = e.detail;
  if (name === "investment_distribution") {
    console.log(name, args);
    dash_clientside.set_props("investment-data", {data: args});
    callback("Investment distribution updated");
  } else if (name === "profile_update") {
    console.log(name, args);
    for (const [key, value] of Object.entries(args)) {
      dash_clientside.set_props(key, {value: value});
    }
    dash_clientside.set_props("profile-data", {data: args});
    callback("Profile information updated");
  } else if (name === "forecast-data") {
    dash_clientside.set_props("forecast-data", {data: args});
    callback("Forecast data updated");
  }
  else if (name === "future_investment_distribution") {
    dash_clientside.set_props("future_investment_distribution", {data: args});
    callback("Forecast distribution updated");
  }
});