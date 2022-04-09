import { BrowserRouter as Router, Route, Routes} from 'react-router-dom'

import Customers from "./components/Customers";
import Customer from "./components/Customer";
import Navigation from "./components/Navigation";
import Incident from './components/Incident';
import CreateCustomer from './components/CreateCustomer';
import CreateIncident from './components/CreateIncident';
import CreateEvidence from './components/CreateEvidence'

export default function App() {
  return (
    <Router>
      <div className='App'>
      <Navigation></Navigation>
        <Routes>
          <Route path="/customer" element={<Customers />}></Route>
            <Route path="/customer/create" element={<CreateCustomer />}></Route>
            <Route path="/customer/:customerId" element={<Customer />}></Route>
            <Route path="/customer/:customerId/createincident" element={<CreateIncident />}></Route>
          <Route path="/incident" element={<Incident />}></Route>
            <Route path="/incident/:incidentId" element={<Incident />}></Route>
            <Route path="/incident/:incidentId/createEvidence" element={<CreateEvidence />}></Route>            
        </Routes>
      </div>
    </Router>
  )
}