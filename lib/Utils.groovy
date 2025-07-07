class Utils {
    // run spooker for the workflow
    public static String spooker(workflow) {
        def pipeline_name = "${workflow.manifest.name.tokenize('/')[-1]}"
        def out = new StringBuilder()
        def err = new StringBuilder()
        def spooker_in_path = check_command_in_path("spooker")
        if (spooker_in_path) {
            try {
                println "Running spooker"
                def spooker_command = "spooker --outdir ${workflow.launchDir} --name ${pipeline_name} --version ${workflow.manifest.version} --path ${workflow.projectDir}"
                def command = spooker_command.execute()
                command.consumeProcessOutput(out, err)
                command.waitFor()
            } catch(IOException e) {
                err = e
            }
            new FileWriter("${workflow.launchDir}/log/spooker.log").with {
                write("${out}\n${err}")
                flush()
            }
        } else {
            err = "spooker not found, skipping"
        }
        return err
    }
    // check whether a command is in the path
    public static Boolean check_command_in_path(cmd) {
        def command_string = "command -V ${cmd}"
        def out = new StringBuilder()
        def err = new StringBuilder()
        try {
            def command = command_string.execute()
            command.consumeProcessOutput(out, err)
            command.waitFor()
        } catch(IOException e) {
            err = e
        }
        return err.length()==0

    }
}
