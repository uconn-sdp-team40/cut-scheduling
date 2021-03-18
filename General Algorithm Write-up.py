# Assume due date and priority number takes priority over filling up all space on tables

order_list = ["Assume filled with order objects"]
# Take input for table lengths.  for now assume 3 of length 100
table_lengths = [100, 100, 100]
time_to_move = 15
current_table_iter = 0  # Assume start at first table aka position 0 - assume for now, but could
#                         take this as an input later if we really wanted to
# sort order list by due date, priority number, time to cut
# Basically just use sorting from earlier example code
# .....

# Divide into sublists - each sublist should have orders of the same due date and priority number, but
# possibly different cut times
# Start iterator at first position aka 0
i = 0
# start with empty queue:
queue = []
# and new order list to add sorted sublists to
new_order_list = []
while i < len(order_list):
    due_date = order_list[i]._due_date
    priority_num = order_list[i]._priority_number
    sublist = []
    sublist.append(order_list[i], 0)
    for j in range(i, len(order_list)):
        # check each
        if order_list[j]._due_date == due_date and order_list[j]._priority_number == priority_num:
            # Append order, along with spot to set as calculated wait / "in-between" time when sorting further down
            # After further work, sublist doesn't actually have to be a list of lists
            # So, the spot for in between time can be removed - but this will require
            # Reformatting any reference to objects in the sublist
            sublist.append([order_list[j], 0])
            # del order_list[j]
            i += 1  # increment i so we will start from the next batch upon finding
            #         orders with different priority or due date
        else:
            break
            # break upon finding orders with different priority or due date

    # begin placing orders in queue
    # continue going through sublist to find next order until we have emptied the list
    while sublist:

        # Possible improvement: select first order to be spread as one that will take least spreading time
        # (and most cutting time if multiple have the least spread time)
        # Only do so if queue is empty
        if not queue:
            first_order = None
            while first_order is None:
                for x in sublist:
                    if ((first_order is None) or (x[0]._spread_time < first_order._spread_time and
                                                  x[0]._cut_time > first_order._cut_time)) \
                            and table_lengths[current_table_iter] <= x[0]._length:
                        first_order = x
            # add found first order to queue
            queue.append([first_order[0], first_order[0]._cut_time, current_table_iter])
            # remove added order from sublist, add to new order list
            sublist.remove(first_order)
            new_order_list.append([first_order[0], current_table_iter])
            # subtract length of first order from table being spread on
            table_lengths[current_table_iter] -= first_order[0]._length
        # As of now, above assume any empty table will be large enough to accommodate any one order

        next_order = None
        next_order_table_index = None
        min_cutter_downtime = float('inf')
        max_cut_time = 0
        min_spread_wait_time = float('inf')
        # calculate current table wait times
        table_cut_wait_times = [0, 0, 0]            # only used for finding cutter down times
        table_cutter_move_wait_times = [0, 0, 0]    # only used for finding cutter down times
        for order in queue:
            table_cut_wait_times[order[2]] += order[1]
        # if a table is not the table the cutter is currently at
        for i in range(0, len(table_lengths)):
            if i != current_table_iter:
                table_cutter_move_wait_times[i] += time_to_move
        for x in sublist:
            table_spread_wait_times = [0, 0, 0]
            table_lengths_copy = [0, 0, 0]
            for i in range(0, len(table_lengths)):
                table_lengths_copy[i] = table_lengths[i]
            for i in range(0, len(table_lengths_copy)):
                if table_lengths_copy[i] < x[0]._length:
                    needed_length = x[0]._length
                    length_avail = table_lengths_copy[i]
                    for y in queue:
                        if length_avail < needed_length:
                            if y[2] == i:
                                table_spread_wait_times[i] += y[1]
                                length_avail += y[0]._length
                        else:
                            break
            # At this point we should now have:
            # - cut wait times for each table, if any
            # - cutter moving time for each table
            # - wait times for spreading for each table, for this specific order
            # We want to minimize cutter down time and spreading wait time
            # Minimizing cutter down time will take priority
            cur_cutter_downtimes = [0, 0, 0]
            for i in range(0, len(cur_cutter_downtimes)):
                cur_cutter_downtimes[i] = table_spread_wait_times[i] \
                                          - table_cut_wait_times[i] \
                                          + table_cutter_move_wait_times[i]
            # In order of precedence:
            # 1. Minimize cutter down time
            # 2. Maximize order cut time (per original priority instructions)
            # 3. Minimize spread wait time
            # We now find which table, for this specific order, would best meet these requirements
            order_min_cutter_downtime = float('inf')
            order_cut_time = x[0]._cut_time
            order_min_spread_wait_time = float('inf')
            table_index = None
            for i in range(0, len(table_lengths)):
                if cur_cutter_downtimes[i] > order_min_cutter_downtime:
                    pass
                elif cur_cutter_downtimes[i] == order_min_cutter_downtime:
                    if table_spread_wait_times[i] >= order_min_spread_wait_time:
                        pass
                    else:
                        order_min_spread_wait_time = table_spread_wait_times[i]
                        table_index = i
                        order_min_cutter_downtime = cur_cutter_downtimes[i]
                elif cur_cutter_downtimes[i] < order_min_cutter_downtime:
                    order_min_spread_wait_time = table_spread_wait_times[i]
                    table_index = i
                    order_min_cutter_downtime = cur_cutter_downtimes[i]
            # after this, we compare to the current values for the next order to be
            # Again, if this order better meets the requirements for the current next order, we replace the current
            # With this new one
            if order_min_cutter_downtime > min_cutter_downtime:
                pass
            elif order_min_cutter_downtime == min_cutter_downtime:
                if order_cut_time < max_cut_time:
                    pass
                elif order_cut_time == max_cut_time:
                    if order_min_spread_wait_time >= min_spread_wait_time:
                        pass
                    elif order_min_spread_wait_time < min_spread_wait_time:
                        next_order = x[0]
                        next_order_table_index = table_index
                        min_cutter_downtime = order_min_cutter_downtime
                        max_cut_time = order_cut_time
                        min_spread_wait_time = order_min_spread_wait_time
                elif order_cut_time > max_cut_time:
                    next_order = x[0]
                    next_order_table_index = table_index
                    min_cutter_downtime = order_min_cutter_downtime
                    max_cut_time = order_cut_time
                    min_spread_wait_time = order_min_spread_wait_time
            elif order_min_cutter_downtime < min_cutter_downtime:
                next_order = x[0]
                next_order_table_index = table_index
                min_cutter_downtime = order_min_cutter_downtime
                max_cut_time = order_cut_time
                min_spread_wait_time = order_min_spread_wait_time

        # The above will occur for every order in the sublist
        # By the time it is done, we should have the order that has:
        # - The least cutter down time
        # - The longest time required to actually cut the order
        # - The minimal spreading wait time
        # We can now add this order to the end of the new order list
        # After doing so we will have to see if other orders have been completed and,
        # if so, remove them from the queue so it will reflect the state of the tables when
        # We look for the next order that should be spread

        # Add to new order list with table index
        new_order_list.append([next_order, next_order_table_index])
        # Add to queue
        queue.append([next_order, next_order._cut_time, next_order_table_index])
        # remove from sublist
        sublist.remove(next_order)
        # subtract spreading time of this order from oldest order in queue if there is one
        if len(queue) > 1:
            queue[0] = [queue[0][0], queue[0][1] - next_order._spread_time, queue[0][2]]
            # if resulting time is negative, remove from queue and subtract (add negative) leftover time
            # from next oldest order if next oldest order is not the new order
            if queue[0][1] <= 0:
                # new order check
                if queue[1][0] == next_order:
                    table_lengths[queue[0][2]] += queue[0]._length
                    queue.pop(0)
                else:
                    while queue[0][1] <= 0:
                        if queue[0][2] == queue[1][2]:
                            queue[1][1] += queue[0][1]
                            # also re-add length to table that is now being cleared
                            table_lengths[queue[0][2]] += queue[0]._length
                            queue.pop(0)
                        else:
                            queue[1][1] += queue[0][1] + time_to_move
                            # also re-add length to table that is now being cleared
                            table_lengths[queue[0][2]] += queue[0]._length
                            queue.pop(0)

# Export new_order_list
# for now, just print
print(new_order_list)