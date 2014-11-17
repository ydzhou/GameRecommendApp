GameRecommendApp
================

A missing game recommender for Steam users who have suffered a long painful way to find a new and awesome game, in the flood of biased and exaggerated comments and recommendations online.

Website: http://gamesyoumiss.herokuapp.com/recom/

FAQ
===

* What is this site?
It recommends games you might be interested in from what your friends on Steam have recently played

* Why we have this site?
Everyday new game is born and they all looks so awesome. The comments and recommendation online are so un-reliable and biased. It is painful to get the right games from those recommendations.

* Then why we can get right games from this site?
People only spend time on things they love to do. When your friends play hundreds of hours on a new game, there is no doubt to try it out. Our site only recommend the games your friends love, and you are most likey to be interested in.

* OK, sounds good, but what is Steam?
It's not water, buddy.

* Give me some spec on this application.
This application is built upon Django framework. It has been deployed on Heroku. Its recommender is a naive-bayes-classifier-based information retrieval program written in Python. It fetches game information from users' Steam profile via Steam Web API to train naive bayes classifier. The game and user information is stored in a Postgres database for future re-use.
