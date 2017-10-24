import React from 'react';
import {render} from 'react-dom';
import MainComponent from './main_component.jsx';

class App extends React.Component {
  render () {
    return (
      <div>
        <MainComponent />
      </div>
    );
  }
}

render(<App/>, document.getElementById('app'));