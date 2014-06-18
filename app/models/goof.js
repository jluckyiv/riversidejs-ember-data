import DS from 'ember-data';

var Goof = DS.Model.extend({
  description: DS.attr('string'),
  minutes: DS.attr('number'),
  seconds: DS.attr('number'),
  movie: DS.belongsTo('movie', {async: true})
});

Goof.reopenClass({
  FIXTURES: [
    {
      id: 1,
      description: 'Scorpion\'s spear disappearing from hand',
      minutes: 45,
      seconds: 30,
      movie: 1
    },
    {
      id: 2,
      description: 'Some goof',
      minutes: 30,
      seconds: 3,
      movie: 2
    },
    {
      id: 3,
      description: 'Another goof',
      minutes: 32,
      seconds: 10,
      movie: 3
    }
  ]
});

export default Goof;
