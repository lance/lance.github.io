const ID = Symbol('id');

class Product {
  constructor (name) {
    this[ID] = 2340847;
  }
  related () {
    return lookupRelatedStuff( this[ID] );
  }
}
