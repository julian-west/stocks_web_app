# stocks_web_app
Plotly-dash web application: Create a custom weighted index to evaluate group of semiconductor stocks

Currently tracks the following stocks:
  - Applied Materials (AMAT)
  - Lam Research (LRCX)
  - ASM international (ASM)
  - Tokyo Electron (8035.T)

### Web app link
https://stock-analysis-web-app.herokuapp.com/

> Note: The app is hosted on a small (free!) dyno hosted by Heroku. If the app doesn't work, try again later or refresh the page a few times until the dyno has woken up again ;).

![gif](./assets/web-app.gif)


### Running locally

```
# install requirements
pip install -r requirements.txt

# install local package
pip install -e .

# run app
python src/app.py
```

### Future Work

- ~~make into web app (on Heroku)~~
- ~~red and green text for positive or negative growth~~
- tidy up formatting
- individual stocks statistics
- caching of data upload when refreshing the page
- ability for users to upload their own csv of stocks for their own index
- multiple pages for the different indexes
- can choose different time periods for the swarm plot (e.g. weekly, monthly, yearly changes etc.) with dynamic x axis
- consolodate graph formatting/layout into master file
- summary statistics with stock weightings and daily, weekly, monthly, yearly performance in a table
- add unit tests
