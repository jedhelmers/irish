import React from 'react';
import { render } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';  // for the "toBeInTheDocument" matcher
import App from './App';

describe('<App />', () => {
  it('renders without crashing', () => {
    const { getByText, getByAltText } = render(<App />);
    
    // Check if the logo is rendered
    const logo = getByAltText('logo');
    expect(logo).toBeInTheDocument();
    
    // Check if the header text is rendered
    const headerText = getByText('Translate English into Irish');
    expect(headerText).toBeInTheDocument();
    
    // Add other assertions as needed
  });
});
