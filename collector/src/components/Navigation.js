import React from 'react'
import { Navbar, Nav, Container } from 'react-bootstrap';

export default function Navigation() {
  return (
    <Navbar bg="dark" variant="dark">
    <Container>
    <Navbar.Brand href="/">COLLECTOR</Navbar.Brand>
    <Nav className="me-auto">
      <Nav.Link href="/customer">Customers</Nav.Link>
      <Nav.Link href="/incident">Incidents</Nav.Link>
      <Nav.Link href="/new">New</Nav.Link>
    </Nav>
    </Container>
  </Navbar>
  )
}
