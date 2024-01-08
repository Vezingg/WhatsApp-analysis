# WhatsApp-analysis
# WhatsApp-Analyzer
Analyze WhatsApp chat

The script reads an exported WhatsApp chat and then extracts the data. You may need to install some packages before running it.

##### Supported Analysis
----------------------
- Chat Count
- Chat Average
- Member/Sender Rank
- Website/URL/Link Domain Rank
- Word Count and Rank
- Most Used Word by Sender
- Emoji Usage Rank
- Most Used Emoji by Sender
- Timestamp Heatmap
- Attachment Classification (In Android, there is no difference pattern for attachment. But in iOS we can actually classify between Image, Video, Audio, GIF, Sticker, Document and Contact Card)

Read and analyze whatsapp chat
positional arguments:
  FILE                  Chat file path

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Debug mode. Shows details for every parsed line.
  
## Flowchart

           +------------------+
      +----+    Empty line?   +----+
      |    +------------------+    |
      |                            |
      |                            |
  +---v---+                   +----v---+
  |  Yes  | +-----------------+   No   |
  +-------+ |                 +---+----+
            |                     |
  +---------+-+             +-----v-----+
  | Event Log |        +----+    Chat   +----+
  +-----------+        |    +-----------+    |
                       |                     |
                +------v-----+         +-----v------+   +--------------------+
          +-----+Regular Chat+----+    | Attachment +-->+ Clasify Attachment |
          |     +------------+    |    +------------+   +-------+------------+
          v                       v                             |
+---------+---------+   +---------+----------+                  |
|   Starting Line   |   |   Following Line   |                  |
+------+------------+   +-+------------------+                  |
       |                  |                                     |
       |                  |                                     |
       |           +------v-------+                             |
       |           | COUNTER      |                             |
       |           | 1 Chat       |                             |
       +---------->+ 2 Timestamp  +<----------------------------+
                   | 3 Sender     |
                   | 4 Domain     |
                   | 5 Words      |
                   | 6 Attachment |
                   | 7 Emoji      |
                   +-----+--------+
                         |
                         |
                         |
                         v
              +----------+----------------+
              |          Visualize        |
              +---------------------------+
