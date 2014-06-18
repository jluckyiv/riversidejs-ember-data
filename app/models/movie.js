import DS from 'ember-data';

var Movie = DS.Model.extend({
  title: DS.attr('string'),
  year: DS.attr('string'),
  director: DS.attr('string'),
  goofs: DS.hasMany('goof', {async: true})
});

Movie.reopenClass({
  FIXTURES: [
    {
      id: 1,
      title: 'Mortal Kombat',
      year: '1995',
      director: 'Paul W.S. Anderson',
      goofs: [1]
    },
    {
      id: 2,
      title: 'Some movie',
      year: '1994',
      director: 'Some director',
      goofs: [2]
    },
    {
      id: 3,
      title: 'Godfather',
      year: '1976',
      director: 'Francis Ford Coppola',
      goofs: [3]
    }
  ]
});

export default Movie;
