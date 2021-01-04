function ass_seconds_to_time_string(seconds)
    local ret = string.format("ASS %d:%02d:%02d.%02d"
        , math.floor(seconds / 3600)
        , math.floor(seconds / 60) % 60
        , math.floor(seconds) % 60
        , seconds * 100 % 100
    )
    return ret
end

function print_time()
    local time = mp.get_property_number("time-pos")
    if time ~= nil then
        local timestr
        timestr = ass_seconds_to_time_string(time)
        mp.osd_message(timestr, 0.01)
        mp.set_property("options/term-status-msg", timestr)
    end
end

timer = mp.add_periodic_timer(0.01, print_time)

function toggle_print_time()
	if timer:is_enabled() then
		timer:stop()
	else
		timer:resume()
	end
end

mp.add_key_binding('c', 'toggle_print_time', toggle_print_time)
