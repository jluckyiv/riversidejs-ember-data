import Ember from 'ember';

var Router = Ember.Router.extend({
  location: MovieGoofsDbENV.locationType
});

Router.map(function() {
  this.resource('movies', { path: '/' });
  this.resource('movie', { path: '/:movie_id' });
});

export default Router;
