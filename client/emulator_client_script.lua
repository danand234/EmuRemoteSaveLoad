local socket = require("socket.core")

function connect(address, port)
    -- TODO: Add screen message for user due to blocking
    local client, err = socket.tcp()
    if not client then return nil, err end
    local result, err = client:connect(address, port)
    if not result then return nil, err end
    client:settimeout(0)
    return client
end

-- Process any errors that have occurred from the receive data operation.
-- Client timeout is 0 to avoid frame blocking operations, so timeout errors are expected behavior.
-- If connection has failed, attempt to reconnect every minute by counting frames.
-- The global error_tick variable is reset to 0 after a successful connection in pollOnFrame.
function processErrors(err)
    if err and err ~= "timeout" then
        emu.print("[!] ERROR: Client receive failed with error: " .. err)
        -- 60 frames/sec is 1 tick in pollOnFrame, so 60 sequential error_ticks is 1 minute
        if error_tick < 60 then
            error_tick = error_tick + 1
            emu.print("[!] WARN: Error tick: " .. error_tick)
        else
            error_tick = 0
            emu.print("[!] WARN: Attempting single reconnect to server")
            -- TODO: Draw something so the player is aware this is occurring
            client, err = connect(server_host, server_port)
            if err then
                emu.print("[!] ERROR: Failed with with error: " .. err)
            else
                emu.print("[-] INFO: Success!")
            end
        end
    end
end

function processMessage(data)
    --value, nextpos = string.unpack( "I1", data) -- not available in Lua 5.1
    value = data:byte(1)
    emu.print("[-] INFO: Data received: " .. value)
    game_file = library_table[tostring(value)]
    emu.print("[-] INFO: Next game selected: [" .. value .. "] " .. game_file)

    game_path = library_dir .. "/" .. game_file

    emu.print("[-] INFO: Saving current game")
    current_save = savestate.create(2)
    savestate.save(current_save)
    savestate.persist(current_save)

    emu.print("[-] INFO: Loading [" .. value .. "]")
    emu.loadrom(game_path)
    next_save = savestate.create(2)
    savestate.load(next_save)
end

function pollOnFrame()
    -- We dont actually need to poll every single frame, so only run every 60 (roughly once per second)
    if tick < 60 then
        tick = tick + 1
        return
    else tick = 0 end

    if not client then
        emu.print("[!] ERROR: Client socket object not initialized!")
        return nil
    end

    local data, err, partial = client:receive(1)  --("*all")
    processErrors(err)
    -- Lua Socket documentation on partial data is unclear. YOLO
    if not data then
        data = partial
        -- emu.print("[!] WARN: Partial data received: " .. partial)
    end
    if data and string.len(data)>0 then
        error_tick = 0 --reset error count, connection is healthy
        processMessage(data)
    end
end

library_table = {}
server_host = "127.0.0.1"
server_port = 8080
tick = 0
error_tick = 0

working_dir = "../working"
config_file = "library.txt"
config_path = working_dir .. "/" .. config_file
library_dir = "../library"

emu.print("[-] INFO: Loading game library from: " .. config_path)
cfile = io.open(config_path, "r")
for line in cfile:lines() do
    game_id, game_name = line:match("(%d+)_(.+)")
    library_table[game_id] = game_name
    emu.print("[-] INFO: Loaded: [" .. game_id .. "] " .. game_name)
end

-- Load default
init_game_file = library_table["1"]
emu.print("[-] INFO: Loading default game: [1] " .. init_game_file)
init_game_path = library_dir .. "/" .. init_game_file
emu.loadrom(init_game_path)
init_save = savestate.create(1)
savestate.load(init_save)

-- Some odd expected failures as the emulator is starting up.
-- Attempt to connect 10 times.
emu.print("[-] INFO: Attempting initial connection.")
for i=1, 10 do
    client, err = connect(server_host, server_port)
    if err then
        emu.print("[!] ERROR: Failed connection attempt " .. i .. " with error: " .. err)
    else break end
end
if not client then
    emu.print("[!] ERROR: Failed initial connection after too many attempts!")
    return -1
end

emu.print("[-] INFO: Success! Starting server polling.")
emu.print("\n\n")

while true do
    pollOnFrame()
    emu.frameadvance()
end