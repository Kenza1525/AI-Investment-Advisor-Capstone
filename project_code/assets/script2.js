// window.mountChainlitWidget({
//   chainlitServer: "http://localhost:8000",
// });

// window.addEventListener("chainlit-call-fn", (e) => {
//   const { name, args, callback } = e.detail;
//   if (name === "formfill") {
//     console.log(name, args);
//     dash_clientside.set_props("fieldA", {value: args.fieldA});
//     dash_clientside.set_props("fieldB", {value: args.fieldB});

//   } 
//   else if (name === "investment_distribution") {
//     console.log(name, args);
//     dash_clientside.set_props("investment-data", {data: args});
//     callback("Investment distribution updated");
//   }
// });


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
  }
});