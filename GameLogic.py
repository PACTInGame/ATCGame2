def simulate_aircraft_radio_transmissions(planes_at_airport, planes_in_airspace, planes_about_to_enter_airspace):
    planes = planes_at_airport + planes_in_airspace + planes_about_to_enter_airspace

    for plane in planes:
        radio = ""
        if plane.state == 0:
            if plane.progress == 2:
                radio = f"Approach, this is {plane.callsign}, at {plane.altitude} feet. Good day, {plane.callsign}."
            elif plane.progress == 80 and plane.controller == 0:
                radio = f"Approach, requesting Tower frequency, {plane.callsign}."

        elif plane.state == 1:
            if plane.controller == 0 and 2 < plane.progress < 5:
                radio = f"Approach, {plane.callsign}, established, need the Tower frequency."
            elif plane.controller == 0 and plane.progress > 15:
                plane.pilot_stress_level += 0.1
                radio = f"Approach, {plane.callsign}, established, need the Tower immediately frequency."

            if plane.controller == 1:
                if 5 < plane.progress < 10 and not plane.cleared_to_land:
                    radio = f"Tower, {plane.callsign}, requesting clearance to land."
                elif 15 < plane.progress < 20 and not plane.cleared_to_land:
                    radio = f"Tower, requesting landing clearance, {plane.callsign}."
                elif 60 < plane.progress < 65 and not plane.cleared_to_land:
                    radio = f"Tower, requesting immediate landing clearance, {plane.callsign}."
                elif 70 < plane.progress < 75 and plane.cleared_to_land and not plane.wind_given:
                    radio = f"Tower, requesting wind information, {plane.callsign}."

        elif plane.state == 2:
            if not plane.wind_given:
                radio = f"Tower, {plane.callsign}, requesting wind information immediately."

        elif plane.state == 3:
            # TODO plane lands at 10 %, rolls until 50%
            if 55 < plane.progress < 60 and plane.controller == 1:
                radio = f"Tower, landed, requesting ground {plane.callsign}."
            elif plane.progress > 95 and plane.controller == 2:
                radio = f"Ground, at runway, {plane.callsign}."
        elif plane.state == 4:
            if 90 < plane.progress < 95:
                radio = f"Ground, at gate, {plane.callsign}."

        elif plane.state == 5:
            if 60 < plane.progress < 65 and not plane.pushback_and_start_approved:
                radio = f"Ground, requesting pushback and startup, {plane.callsign}."
            if plane.progress > 95 and not plane.cleared_to_runway:
                radio = f"Ground, ready to taxi, {plane.callsign}."

        elif plane.state == 6:
            if 90 < plane.progress < 95 and plane.controller == 2:
                radio = f"Ground, requesting Tower frequency, {plane.callsign}."
            elif plane.progress > 95 and plane.controller == 1:
                radio = f"Tower, at runway, ready for departure, {plane.callsign}."
        elif plane.state == 6.5:
            if 50 < plane.progress < 55:
                radio = f"Tower, {plane.callsign}, still on runway, awaiting departure clearance."
            elif 80 < plane.progress < 85:
                radio = f"Tower, {plane.callsign}, we're still lined up for departure."
            if plane.progress > 55:
                plane.pilot_stress_level += 0.1
        elif plane.state == 7:
            if 50 < plane.progress < 55 and not plane.departure_frequency:
                radio = f"Tower, {plane.callsign}, passing 1500."
            elif 80 < plane.progress < 85 and not plane.departure_frequency:
                radio = f"Tower, {plane.callsign}, passing 3000, requesting departure frequency."
        elif plane.state == 10:
            if plane.progress == 5:
                radio = f"{plane.callsign}, going around."
        dont_add = False
        for transm in plane.atc_history:
            if radio == transm[1]:
                dont_add = True
        if radio != "" and not dont_add:
            plane.atc_history.append([plane.controller, radio, 0])
            print(radio)

            if plane.controller == 0: # TODO contact tower, ground on old freq
                plane.game.UI.approach_communications.append([plane.controller, radio, 0])
            elif plane.controller == 1:
                plane.game.UI.tower_communications.append([plane.controller, radio, 0])
            elif plane.controller == 2:
                plane.game.UI.ground_communications.append([plane.controller, radio, 0])


def atc_calls(call, plane, game, info=""):
    transmission = ""
    if call == 0:
        transmission = f"{plane.callsign}, Approach, good day. Radar contact. Expect ILS approach."  # TODO add runway num
    elif call == 1:
        info = "118.1"
        transmission = f"{plane.callsign}, Approach, cleared ILS approach. Contact Tower on {info}." # TODO Anther contac tower for takeoff
    elif call == 2:
        transmission = f"{plane.callsign}, Tower, cleared to land."
    elif call == 3:
        transmission = f"{plane.callsign}, Tower, wind {game.airport.wind}."
    elif call == 4:
        info = "121.9"
        transmission = f"{plane.callsign}, Tower, exit right when able, contact Ground on {info}."
    elif call == 5:
        transmission = f"{plane.callsign}, Ground, taxi to gate via Taxiway Alpha."
    elif call == 6:
        transmission = f"{plane.callsign}, Ground, pushback and start approved."
    elif call == 7:
        transmission = f"{plane.callsign}, Ground, taxi to and hold short of the runway via TW Bravo."
    elif call == 8:
        info = "118.1"
        transmission = f"{plane.callsign}, Ground, contact tower on {info}."
    elif call == 9:
        transmission = f"{plane.callsign}, Tower, line up and wait."
    elif call == 10:
        transmission = f"{plane.callsign}, Tower, cleared for takeoff."
    elif call == 11:
        info = "122.6"
        transmission = f"{plane.callsign}, Tower, contact Departure on {info}, good day."
    elif call == 12:
        transmission = f"{plane.callsign}, Tower, go around, published missed approach procedure."

    plane.atc_history.append([plane.controller, transmission, 1])
    print(transmission)
    if call <= 1:
        plane.game.UI.approach_communications.append([plane.controller, transmission, 1])
    elif 2 <= call <= 4 or 9 <= call <= 12:
        plane.game.UI.tower_communications.append([plane.controller, transmission, 1])
    elif 5 <= call <= 8:
        plane.game.UI.ground_communications.append([plane.controller, transmission, 1])

    plane_answers(call, plane, info)


def plane_answers(atc_call, plane, info=""):
    radio = f"Unable, {plane.callsign}."
    if atc_call == 0:
        if plane.state == 0:
            radio = f"Expect ILS approach, {plane.callsign}."  # TODO add runway num
            plane.cleared_approach = True
    elif atc_call == 1 or atc_call == 8:
        if (plane.state == 0 and plane.cleared_approach) or plane.state == 6:
            radio = f"Contact Tower on {info}, {plane.callsign}."

    elif atc_call == 2:
        if (plane.state == 1 or plane.state == 0) and plane.controller == 1:
            radio = f"Cleared to land, {plane.callsign}."
            plane.cleared_to_land = True
    elif atc_call == 3:
        if (plane.state == 0 and plane.cleared_approach) or 1 <= plane.state <= 2 or plane.state == 6.5:  # TODO unable returned via wrong channel: No respons if wrong channel
            radio = f"Wind {plane.game.airport.wind}, {plane.callsign}."
            plane.wind_given = True
    elif atc_call == 4:
        if plane.state == 3:
            radio = f"Contact Ground on {info}, {plane.callsign}."
    elif atc_call == 5:
        if plane.state == 3:
            radio = f"Taxi to gate via Taxiway Alpha, {plane.callsign}."
            plane.cleared_to_gate = True
    elif atc_call == 6:
        if plane.state == 5:
            radio = f"Pushback and start approved, {plane.callsign}."
            plane.pushback_and_start_approved = True
    elif atc_call == 7:
        if plane.state == 5:
            radio = f"Taxi to and hold short of the runway via Bravo, {plane.callsign}."
            plane.cleared_to_runway = True
    elif atc_call == 9:
        if plane.state == 6 and plane.controller == 1:
            radio = f"Line up and wait, {plane.callsign}."
            plane.cleared_to_lineup = True
    elif atc_call == 10:
        if (plane.state == 6.5 or (plane.state == 6 and plane.progress > 95)) and plane.controller == 1:
            radio = f"Cleared for takeoff, {plane.callsign}."
            plane.cleared_to_start = True
    elif atc_call == 11:
        if plane.state == 7 and plane.progress > 55:
            radio = f"Contact Departure on {info}, good day, {plane.callsign}."
            plane.departure_frequency = True
    elif atc_call == 12:
        if plane.state == 1 or plane.state == 2:
            radio = f"Go around, published missed approach procedure, {plane.callsign}."
            plane.change_state(11)

    if "Unable" in radio:
        plane.pilot_stress_level += 1

    plane.atc_history.append([plane.controller, radio, 0])
    print(radio)
    if plane.controller == 0:
        plane.game.UI.approach_communications.append([plane.controller, radio, 0])
    elif plane.controller == 1:
        plane.game.UI.tower_communications.append([plane.controller, radio, 0])
    elif plane.controller == 2:
        plane.game.UI.ground_communications.append([plane.controller, radio, 0])

    if "Contact Tower" in radio:
        plane.controller = 1
    elif "Contact Ground" in radio:
        plane.controller = 2
