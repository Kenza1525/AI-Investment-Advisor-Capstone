# AI-Investment-Advisor-Capstone

#----------------------------Update----------------------------------------------

The code files have been reorganized. The files you need now are the ones in tools, agent, assets and the cmu-dash.py

If you clone the repo, here is how you can run the project now.

`python3 -m chainlit run agent/agent.py -w -h`
`python3 cmu-dash.py`

Make sure tools, assets, agent and cmu-dash.py live in the same directory before you run the command above
To run the project,
Clone this repo. Go into the project_code directory. Run the dash app this way `python3 cmu-dash.py`
Run the copilot this way: `python3 -m chainlit run chat-hypo-pilot.py -w -h`
Note: both must be running. You can do that by creatingh two terminal sessions - one for each.

#--------------------------Updates made----------------------------------------------#

I have added a yahoo finance tool. Here is what it does:
1. It gets current market performance summary data from yahoo finance.
2. It groups the different assets returned in the market summary into asset classes along with the price change and percentage change information associated with each asset
3. It then computes a combined normalized values of these two quantities and use that to rank the asset classes in terms of performance.
4. This tool is used to make recommendations to users based on performing asset classes.
5. When personalized investment advise is sought, it combines this information with the user profile information to make the recommendations.
6. It needs a little bit of cleaning up as I still have some inconsistent system prompts and information in the InvestmentTool that contradicts the other tool.
7. This needs fixing for the agent to work well
