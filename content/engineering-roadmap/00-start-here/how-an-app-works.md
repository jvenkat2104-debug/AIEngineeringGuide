# How an app works: from tap to database

Status: Draft | Independent review pending

Suppose you tap **Order** in a food-delivery app. The screen, network request, business rules and stored records have different jobs.

| Part | What it does | Restaurant analogy |
| --- | --- | --- |
| Front end | Collects the tap and displays the result | Dining area and staff |
| API | Defines how the app requests an action | Order slip and agreed ordering process |
| Back end | Checks availability and applies order rules | Kitchen |
| Database | Stores menus, prices and orders | Record book and storeroom |
| Response | Reports the result to the screen | Confirmation from the kitchen |

The app sends a request. The server validates it, processes the order, saves relevant records and returns a response. Real systems may split this into several services; a successful screen update is not a guarantee that every later step has completed.

## The same idea in a device

A smart meter senses a quantity, a microcontroller processes readings, a communication module sends them, and a server stores them. Draw **sensor → controller → network → server → storage** and identify where an invalid or missing reading could occur.

## Try it

Open a public website in a desktop browser, open developer tools and select Network. Reload the page. Pick one request and identify its destination, status and response type. Do not copy authentication headers or private data into a public issue.

On paper, explain what the screen should show if an order fails or a response is delayed. Could retrying accidentally create a duplicate order?

---
Source basis: Campus to Corporate blueprint, Version 4. Adapted for this guide; additions and pathway suggestions require review.
